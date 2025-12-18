import datetime
import logging
import openreview
from .decorators import require_confirmation
from typing import Dict, List, Optional, Callable, Union, Mapping, Sequence
from .note_utils import NoteUtils
from .profile_utils import ProfileUtils
from copy import deepcopy

from .constants import (
    PROFILE_ID_FIELD,
    REGISTRATION_FORM_MAPPING,
    LICENSE_FORM_MAPPING,
    EMERGENCY_FORM_MAPPING,
    LOAD_FORM_MAPPING,
    DEFAULT_REGISTRATION_CONTENT,
    DEFAULT_EMERGENCY_CONTENT
)

logger = logging.getLogger('arr.matching.registration')


class RegistrationDataLoader(object):
    """
    Load registration notedata needed for ARR matching.
    """
    
    def __init__(self, client, venue):
        """
        Initialize the loader with OpenReview client and venue helper.
        
        Args:
            client: OpenReview API client used for note/group reads.
            venue: Venue helper (as used in openreview/arr/matching/core.py).
        """
        self.client = client
        self.venue = venue
    
    def get_research_areas(
        self,
        members: Sequence[str],
        group_id: Optional[str] = None
    ) -> Dict[str, List[str]]:
        """
        Load research areas for a list of members from registration notes.
        
        Given a list of profile IDs, loads notes from relevant invitations
        and returns a mapping from profile_id -> list of research areas.
        
        Args:
            members: Profile names/IDs
            group_id: Optional group ID to load registration notes from. If None, checks all role groups.
            
        Returns:
            Dict[str, List[str]]: Keys are profile IDs, values are research areas.
            
        Raises:
            ValueError: If members cannot be resolved to valid profiles.
        """
        # Normalize members to canonical profile IDs
        profiles = ProfileUtils.get_valid_profiles(self.client, list(members))
        profile_ids = {profile.id for profile in profiles}
        name_to_profile_id = ProfileUtils.map_profile_names_to_profile_id(profiles)
        
        # Load notes from relevant invitations
        # Priority: role registration forms, then author form
        author_notes = []
        
        # Load author form
        try:
            author_form_invitation = f"{self.venue.get_authors_id()}/-/Submitted_Author_Form"
            author_notes = self.client.get_all_notes(invitation=author_form_invitation)
        except Exception as e:
            logger.debug(f"Could not load author forms: {e}")
        
        # Collect registration notes
        all_registration_notes = []
        if group_id:
            # Load from specific group
            try:
                registration_invitation = f"{group_id}/-/Registration"
                notes = self.client.get_all_notes(invitation=registration_invitation)
                all_registration_notes.extend(notes)
            except Exception as e:
                logger.debug(f"Could not load registration notes from {group_id}: {e}")
        else:
            # Check all potential role groups
            potential_groups = [
                self.venue.get_reviewers_id(),
                self.venue.get_area_chairs_id(),
                self.venue.get_senior_area_chairs_id(),
            ]
            for potential_group_id in potential_groups:
                try:
                    registration_invitation = f"{potential_group_id}/-/Registration"
                    notes = self.client.get_all_notes(invitation=registration_invitation)
                    all_registration_notes.extend(notes)
                except Exception as e:
                    logger.debug(f"Could not load registration notes from {potential_group_id}: {e}")
        
        # Map notes to profile IDs
        profile_id_to_notes = {}  # profile_id -> list of (note, timestamp) tuples
        
        # Process registration notes
        for note in all_registration_notes:
            signature = note.signatures[0] if getattr(note, 'signatures', None) else None
            if isinstance(getattr(note, 'content', None), dict) and PROFILE_ID_FIELD in note.content:
                raw = note.content.get(PROFILE_ID_FIELD)
                if isinstance(raw, dict):
                    signature = raw.get('value', signature)
                elif isinstance(raw, str):
                    signature = raw

            profile_id = name_to_profile_id.get(signature)
            if profile_id and profile_id in profile_ids:
                timestamp = note.tmdate
                if profile_id not in profile_id_to_notes:
                    profile_id_to_notes[profile_id] = []
                profile_id_to_notes[profile_id].append((note, timestamp, 'registration'))
        
        # Process author notes
        for note in author_notes:
            signature = note.signatures[0] if getattr(note, 'signatures', None) else None
            if isinstance(getattr(note, 'content', None), dict) and PROFILE_ID_FIELD in note.content:
                raw = note.content.get(PROFILE_ID_FIELD)
                if isinstance(raw, dict):
                    signature = raw.get('value', signature)
                elif isinstance(raw, str):
                    signature = raw

            profile_id = name_to_profile_id.get(signature)
            if profile_id and profile_id in profile_ids:
                timestamp = note.tmdate
                if profile_id not in profile_id_to_notes:
                    profile_id_to_notes[profile_id] = []
                profile_id_to_notes[profile_id].append((note, timestamp, 'author'))
        
        # Extract research areas - use most recent note
        profile_id_to_research_areas = {}
        notes_loaded_total = len(all_registration_notes) + len(author_notes)
        mapped_members = 0
        missing_members = []
        
        for profile_id in profile_ids:
            if profile_id not in profile_id_to_notes:
                missing_members.append(profile_id)
                continue
            
            # Sort notes by timestamp (most recent first)
            notes_with_timestamps = profile_id_to_notes[profile_id]
            notes_with_timestamps.sort(key=lambda x: x[1], reverse=True)
            
            # Try to extract research areas from most recent note
            research_areas = None
            for note, timestamp, source in notes_with_timestamps:
                try:
                    # Try registration note field first
                    if 'research_area' in note.content:
                        research_areas = note.content['research_area'].get('value', [])
                        break
                    # Try author form field
                    if 'indicate_your_research_areas' in note.content:
                        research_areas = note.content['indicate_your_research_areas'].get('value', [])
                        break
                except (KeyError, TypeError, AttributeError) as e:
                    logger.debug(f"Error extracting research areas from note {note.id}: {e}")
                    continue

                if research_areas:
                    profile_id_to_research_areas[profile_id] = research_areas
                    mapped_members += 1
                else:
                    missing_members.append(profile_id)
        
        logger.info(f"get_research_areas: notes_loaded_total={notes_loaded_total}, "
                   f"mapped_members={mapped_members}, missing_members={len(missing_members)}")
        
        return profile_id_to_research_areas
    
    def get_loads(
        self,
        members: Sequence[str],
        forced_loads: Optional[Mapping[str, int]] = None,
        group_id: Optional[str] = None
    ) -> Dict[str, int]:
        """
        Load max loads for a list of members from load notes, applying forced overrides.

        Searches across all load notes
        
        Args:
            members: Profile names/IDs
            forced_loads: Optional mapping from user identifier/profile id to forced capacity.
                         Override semantics: forced value wins over note-derived value.
            group_id: Optional group ID to load notes from. If None, checks all role groups.
        
        Returns:
            Dict[str, int]: Keys are canonical profile IDs, values are non-negative ints.
            
        Raises:
            ValueError: For invalid forced_loads values (non-int or negative).
            ValueError: If member profiles cannot be resolved.
        """
        # Validate forced_loads
        if forced_loads:
            for member_id, load_value in forced_loads.items():
                if not isinstance(load_value, int) or load_value < 0:
                    raise ValueError(f"Invalid forced_load value for {member_id}: {load_value} must be non-negative int")
        
        # Normalize members to profile IDs
        profiles = ProfileUtils.get_valid_profiles(self.client, list(members))
        profile_ids = {profile.id for profile in profiles}
        name_to_profile_id = ProfileUtils.map_profile_names_to_profile_id(profiles)
        
        # Normalize forced_loads keys to profile IDs
        normalized_forced_loads = {}
        if forced_loads:
            for member_id, load_value in forced_loads.items():
                # Try direct match first
                if member_id in profile_ids:
                    normalized_forced_loads[member_id] = load_value
                elif member_id in name_to_profile_id:
                    profile_id = name_to_profile_id[member_id]
                    normalized_forced_loads[profile_id] = load_value
                else:
                    logger.warning(f"forced_loads contains non-member: {member_id}, ignoring")

        
        all_load_notes = []
        if group_id:
            try:
                load_invitation = f"{group_id}/-/Max_Load_And_Unavailability_Request"
                notes = self.client.get_all_notes(invitation=load_invitation)
                all_load_notes.extend(notes)
            except Exception as e:
                logger.debug(f"Could not get load notes from {group_id}: {e}")
        else:
            # Check all potential role groups
            potential_groups = [
                self.venue.get_reviewers_id(),
                self.venue.get_area_chairs_id(),
                self.venue.get_senior_area_chairs_id(),
            ]
            for potential_group_id in potential_groups:
                try:
                    load_invitation = f"{potential_group_id}/-/Max_Load_And_Unavailability_Request"
                    notes = self.client.get_all_notes(invitation=load_invitation)
                    all_load_notes.extend(notes)
                except Exception as e:
                    logger.debug(f"Could not load load notes from {potential_group_id}: {e}")
        
        # Map notes to profile IDs
        profile_id_to_note = {}
        
        for note in all_load_notes:
            signature = note.signatures[0] if getattr(note, 'signatures', None) else None
            if isinstance(getattr(note, 'content', None), dict) and PROFILE_ID_FIELD in note.content:
                raw = note.content.get(PROFILE_ID_FIELD)
                if isinstance(raw, dict):
                    signature = raw.get('value', signature)
                elif isinstance(raw, str):
                    signature = raw

            profile_id = name_to_profile_id.get(signature)
            if profile_id and profile_id in profile_ids:
                # If multiple notes exist, keep the most recent one
                if profile_id not in profile_id_to_note:
                    profile_id_to_note[profile_id] = note
                else:
                    # Compare timestamps
                    existing_timestamp = profile_id_to_note[profile_id].tmdate
                    new_timestamp = note.tmdate
                    if new_timestamp > existing_timestamp:
                        profile_id_to_note[profile_id] = note
        
        # Extract loads
        profile_id_to_loads = {}
        notes_loaded_total = len(all_load_notes)
        overrides_applied = 0
        invalid_load_values = 0
        
        for profile_id in profile_ids:
            # Check forced_loads first
            if profile_id in normalized_forced_loads:
                profile_id_to_loads[profile_id] = normalized_forced_loads[profile_id]
                overrides_applied += 1
                continue
            
            # Try to extract from note
            if profile_id in profile_id_to_note:
                note = profile_id_to_note[profile_id]
                try:
                    load_value = note.content.get('maximum_load_this_cycle', {}).get('value')
                    if load_value is not None:
                        load_int = int(load_value)
                        if load_int >= 0:
                            profile_id_to_loads[profile_id] = load_int
                        else:
                            invalid_load_values += 1
                            logger.warning(f"Negative load value for {profile_id}: {load_int}")
                    else:
                        invalid_load_values += 1
                except (ValueError, TypeError, KeyError) as e:
                    invalid_load_values += 1
                    logger.debug(f"Error extracting load from note {note.id}: {e}")
        
        logger.info(f"get_loads: notes_loaded_total={notes_loaded_total}, "
                   f"overrides_applied={overrides_applied}, invalid_load_values={invalid_load_values}")
        
        return profile_id_to_loads


def transfer_between(
    from_group: str,
    to_group: str,
    members: Optional[Sequence[str]],
    client: openreview.api.OpenReviewClient,
    dry_run: bool = False
) -> Dict[str, int]:
    """
    Transfer members from one group to another
    
    Only removes members present in from_group
    and only adds members missing from to_group.
    
    Args:
        from_group: Source group id.
        to_group: Target group id.
        members: Explicit list of members to transfer (required, cannot be None).
        client: OpenReview API client.
        dry_run: If True, do not mutate group membership.
    
    Returns:
        Dict[str, int] with summary counts:
        - members_added: Number of members added to to_group
        - members_removed: Number of members removed from from_group
        - members_skipped_not_in_source: Number of members not in from_group
        - members_skipped_already_in_target: Number of members already in to_group
    
    Raises:
        ValueError: If members is None (explicit list required).
    """
    if members is None:
        raise ValueError("members parameter is required and cannot be None")
    
    # Normalize members to canonical profile IDs
    profiles = ProfileUtils.get_valid_profiles(client, list(members))
    profile_ids = [profile.id for profile in profiles]
    name_to_profile_id = ProfileUtils.map_profile_names_to_profile_id(profiles)
    name_to_all_names = ProfileUtils.map_profile_names_to_all_names(profiles)
    
    # Build reverse mapping: all names -> canonical profile ID
    name_to_profile_id = {}
    for name, all_names in name_to_all_names.items():
        canonical_id = name_to_profile_id[name]
        for alt_name in all_names:
            name_to_profile_id[alt_name] = canonical_id
    
    # Get current group memberships
    from_group_obj = client.get_group(from_group)
    to_group_obj = client.get_group(to_group)
    
    # Normalize group members to canonical IDs for comparison
    def normalize_group_members(group_members):
        """Normalize group members to canonical profile IDs."""
        normalized = set()
        profiles_for_group = openreview.tools.get_profiles(client, group_members)
        for profile in profiles_for_group:
            normalized.add(profile.id)
            # Also add all alternate names
            for name_obj in profile.content.get('names', []):
                if 'username' in name_obj:
                    normalized.add(name_obj['username'])
        return normalized
    
    from_group_members_set = normalize_group_members(from_group_obj.members)
    to_group_members_set = normalize_group_members(to_group_obj.members)
    
    # Determine actions
    members_to_remove = []
    members_to_add = []
    members_skipped_not_in_source = 0
    members_skipped_already_in_target = 0
    
    # Build profile_id -> all_names mapping
    profile_id_to_all_names = {}
    for profile in profiles:
        all_names = [
            name_obj['username']
            for name_obj in profile.content.get('names', [])
            if 'username' in name_obj and len(name_obj['username']) > 0
        ]
        profile_id_to_all_names[profile.id] = all_names
    
    for profile_id in profile_ids:
        # Get all names for this profile
        all_names_for_profile = profile_id_to_all_names.get(profile_id, [profile_id])
        
        # Check if member is in source group (by any name)
        in_source = False
        for name in all_names_for_profile:
            if name in from_group_members_set:
                in_source = True
                break
        
        # Check if member is already in target group (by any name)
        in_target = False
        for name in all_names_for_profile:
            if name in to_group_members_set:
                in_target = True
                break
        
        if not in_source:
            members_skipped_not_in_source += 1
        elif in_target:
            members_skipped_already_in_target += 1
        else:
            # Need to transfer
            # Find the actual member identifier in from_group
            actual_from_member = None
            for name in all_names_for_profile:
                if name in from_group_obj.members:
                    actual_from_member = name
                    break
            
            if actual_from_member:
                members_to_remove.append(actual_from_member)
            members_to_add.append(profile_id)
    
    # Execute transfers
    members_added = 0
    members_removed = 0
    
    if not dry_run:
        # Remove from source group
        for member in members_to_remove:
            if member in from_group_obj.members:
                client.remove_members_from_group(from_group_obj, member)
                members_removed += 1
        
        # Add to target group
        for member in members_to_add:
            if member not in to_group_obj.members:
                client.add_members_to_group(to_group_obj, member)
                members_added += 1
    
    logger.info(f"transfer_between: members_added={members_added}, members_removed={members_removed}")
    
    return {
        'members_added': members_added,
        'members_removed': members_removed,
        'members_skipped_not_in_source': members_skipped_not_in_source,
        'members_skipped_already_in_target': members_skipped_already_in_target
    }
