async function process(client, edit, invitation) {
    client.throwErrors = true
    
    const { note } = edit

    if (note.ddate) { 
      return
    }

    const profiles = await client.tools.getProfiles(note.content.authorids.value)
    const profileIds = profiles.map(profile => profile.id)

    const primaryAuthorField = note.content.corresponding_author.value
    const primaryAuthorProfile = await client.tools.getProfiles([primaryAuthorField])
    const primaryAuthor = primaryAuthorProfile[0].id
    if (!profileIds.includes(primaryAuthor)) {
      return Promise.reject(new OpenReviewError({ name: 'Error', message: 'Select a paper co-author as corresponding author, ' + primaryAuthorField + ' does not appear in the author list' }))
    }

    if (note.content.financial_support) {
      const financialSupportField = note.content.financial_support.value
      const financialSupportProfile = await client.tools.getProfiles([financialSupportField])
      const financialSupport = financialSupportProfile[0].id
      if (!profileIds.includes(financialSupport)) {
        return Promise.reject(new OpenReviewError({ name: 'Error', message: 'Select a paper co-author for financial support, ' + financialSupportField + ' does not appear in the author list' }))
      }
    }

    const reviewerNominationField = note.content.reviewer_nomination.value
    const reviewerNominationProfile = await client.tools.getProfiles([reviewerNominationField])
    const reviewerNomination = reviewerNominationProfile[0].id
    if (!profileIds.includes(reviewerNomination)) {
      return Promise.reject(new OpenReviewError({ name: 'Error', message: 'Select a paper co-author to nominate as reviewer, ' + reviewerNominationField + ' does not appear in the author list' }))
    }

    const { groups: revGroups } = await client.getGroups({ id: invitation.domain + '/Reviewers' })
    const reviewers = revGroups[0].members;
    
    const reviewerMembers = {}
    for (const reviewer of reviewers) {
      reviewerMembers[reviewer] = true
    }

    const { groups: acGroups } = await client.getGroups({ id: invitation.domain + '/Area_Chairs' })
    const acs = acGroups[0].members;
    
    const acMembers = {}
    for (const ac of acs) {
      acMembers[ac] = true
    }

    for (const profile of profiles) {
      const emails = profile.content.emails
      const usernames = profile.content.names.map(name => name.username)
      const allIds = emails.concat(usernames)
      for (const username of allIds) {
        if (reviewerMembers[username]) {
          const { count: noteCount } = await client.getNotes({ invitation: 'NeurIPS.cc/2023/Conference/Reviewers/-/Registration', signatures: [allIds] })
          if (noteCount === 0) {
            return Promise.reject(new OpenReviewError({ name: 'Error', message: 'Reviewer ' + client.tools.prettyId(username) + ' has not completed the Reviewer Registration.' }))
          }
        }
        if (acMembers[username]) {
          const { count: noteCount } = await client.getNotes({ invitation: 'NeurIPS.cc/2023/Conference/Area_Chairs/-/Registration', signatures: [allIds] })
          if (noteCount === 0) {
            return Promise.reject(new OpenReviewError({ name: 'Error', message: 'Area chair ' + client.tools.prettyId(username) + ' has not completed the Area Chair Registration.' }))
          }
        }
      }
    }
}