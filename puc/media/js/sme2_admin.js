function valida(opcao) {

	var f=document.frm;
	var f2=document.frm2;

	if (f.produto.value == "0"){
		window.alert("ATENÇÃO\n\nPor favor informe o produto.");
		f.produto.focus();
		return;
	}

	if (f.alarme.value == "0"){
		window.alert("ATENÇÃO\n\nPor favor informe o alarme.");
		f.alarme.focus();
		return;
	}

	if (f.monitor.value == "0"){
		window.alert("ATENÇÃO\n\nPor favor informe o monitor.");
		f.monitor.focus();
		return;
	}

	f2.target = "_blank";
	f2.submit();
}

function adicionaAlarmes(idprod){ //idProduto
	if (idprod != 0) {
		removeAlarmes();
		var f = document.frm;
		//carregamos os alarmes com o json
		f.alarme.options[0] = new Option("[Selecione um alarme]");
		f.alarme.options[0].value = "0"; 
		var array = produtos_alarmes_json[idprod]
		//console.log(array)
		for(i=0; i<array.length; i++) {
				var novo= f.alarme.options.length; 
				f.alarme.options[novo] = new Option(array[i].alm_nome);
				f.alarme.options[novo].value = array[i].alm_id; 
				//if (array[i][3] =="SELECTED") f.alarme.options[novo].selected = true;
		}
		removeMonitores();
		f.monitor.options[0] = new Option("[Selecione um monitor]");
		f.monitor.options[0].value = "0";
	}
}

function removeAlarmes(){
	var f = document.frm;
	if (f.alarme.options.length>0) f.alarme.options.length=0;
}

function removeProdutos(){
	var f = document.frm;
	if (f.produto.options.length>0) f.produto.options.length=0;
}

function removeAcoes(){
	var f = document.frm;
	if (f.acao_id.options.length>0) f.acao_id.options.length=0;
}

function trataAcao(id_acao){

	if (id_acao == 2) {
		var f = document.frm;
		if ( f.produto.value != 0 && f.alarme.value != 0 && f.monitor.value != 0) {
			f.action = "?pagina=1";
			f.submit();
		} else {
			alert('Por favor preencher todos os campos\n antes de selecionar a ação.');
			f.acao_id.value = 0;
		}
	} else if ( id_acao == 1) {
		limpaEventos();
	} else {
		limpaEventos();
	}
}

function trataPaginacao(uri) {
	var f = document.frm;
	f.action = uri;
	f.submit();
}

function limpaEventos() {
	c = document.getElementById('id-eventos');
	c.innerHTML = "";
}

function trataCancelar() {
	var f = document.frm;
	f.action = "";
	f.method = "GET";
	removeAcoes();
	removeProdutos();
	removeAlarmes();
	removeMonitores();
	f.submit();
}


function adicionaMonitores(idalar){ //idProduto
	if (idalar != 0) {
		removeMonitores();
		var f = document.frm;
		//carregamos os monitores com o json
		f.monitor.options[0] = new Option("[Selecione um monitor]");
		f.monitor.options[0].value = "0"; 
		var array = alarmes_monitores_json[idalar]
		for(i=0; i<array.length; i++) {
				var novo= f.monitor.options.length; 
				f.monitor.options[novo] = new Option(array[i].mon_nome);
				f.monitor.options[novo].value = array[i].mon_id; 
				//if (array[i][3] =="SELECTED") f.alarme.options[novo].selected = true;
		}	
	}
}

function removeMonitores(){
	var f = document.frm;
	if (f.monitor.options.length>0) f.monitor.options.length=0;
}
