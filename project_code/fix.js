
//deze push dingen in deze functie zetten
function create_table(head, data, need_textbox) {
	head.push("PMID's");
	data.push(kut_koen());
	need_textbox.push("PMID's");


//deze functie ergens neerzetten
function kut_koen() {
	ids = [];
	aantal =10;
	for (j=0; j<aantal; j++ ) {
		id = "PMID";
		for (i=0; i < 8; i++) {
    		random_numb = Math.floor((Math.random() * 10) + 1);
    		id += random_numb + "&#13;&#10;";
    }
    ids.push(id)
	}
	return ids
}
