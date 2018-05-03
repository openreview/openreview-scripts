
// ------------------------------------
// Basic venue homepage template
//
// This webfield displays the conference header (#header), the submit button (#invitation),
// and a list of all submitted papers (#notes).
// ------------------------------------


// Main is the entry point to the webfield code and runs everything
function main() {
  Webfield.ui.setup('#group-container', 'ICML.cc/2018/Workshop/NAMPI');  // required

  renderConferenceHeader();

}

// RenderConferenceHeader renders the static info at the top of the page. Since that content
// never changes, put it in its own function
function renderConferenceHeader() {
  Webfield.ui.venueHeader({
    title: 'NAMPI: Neural Abstract Machines & Program Induction',
    subtitle: 'A Federated Artificial Intelligence Meeting (FAIM) workshop (ICML, IJCAI/ECAI, AAMAS)',
    location: 'Stockholm, Sweden',
    date: '2018',
    website: 'https://uclmr.github.io/nampi/',
    instructions: 'Check back later for details',  // Add any custom instructions here. Accepts HTML
    deadline: 'TBD'
  });
}

// Go!
main();

