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

	if(f2.diaInicio.value == 0 || f2.mesInicio.value == 0 || f2.anoInicio.value == 0 || f2.diaFim.value == 0 || f2.mesFim.value == 0 || f2.anoFim.value == 0){
		window.alert("ATENÇÃO\n\nPor favor informe as datas de início e fim do período.");
		f2.diaInicio.focus();
		return;
	}

	//se opcao for e-exportacao
	if (opcao=='e') {
		f2.action = f2.relcsv.value;
	} 
	else{
		f2.action = f2.reljsp.value;
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
	}
}

function removeAlarmes(){
	var f = document.frm;
	if (f.alarme.options.length>0) f.alarme.options.length=0;
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