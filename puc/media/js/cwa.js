/*Funcao para adicionar o efeito do slide nos boxes*/
function init() {
	//console.log("body loaded")
	
	var visoes_estado = {
		"block-tabular" : false, 
		"block-hierarquica" : false,
		"block-relatorio" : false
	};

	var container_conteudo = {
		"portal-column-0" : '', 
		"portal-column-1" : '',
		"portal-column-bottom" : ''
	};
	
	/*
	for (var c in visoes_estado) {
		console.log(c + '->' + visoes_estado[c])
	}
	*/
		
	this.options = {
      portal: 'portal',
      column: 'portal-column',
      block: 'block',
      content: 'content',
      handle: 'handle',
      hoverclass: 'block-hover',
      toggle: 'block-toggle',
      blocklist: 'portal-column-block-list',
      blocklistlink: 'portal-block-list-link',
      blocklisthandle: 'block-list-handle',
    }

    var blocks = document.getElementsByClassName(
      this.options.block, this.options.portal
    );
    
	/*
	for (var container in settings) {
	  visoes = settings[container]
	  len_visoes = visoes.length
	  if (len_visoes > 0) {
			visoes.each(function (block) {
				//c = document.getElementById(container)
				//conteudo = container_conteudo[container];
				//conteudo = conteudo + '<div class="block" id="' + block + '">\n';
				//conteudo = conteudo + $(block).innerHTML;
				//conteudo = conteudo + '</div>'
				//console.log(conteudo)
				//c.innerHTML = conteudo;
				//console.log(container+' -> '+block)
				$(container).appendChild($(block));     
				visoes_estado[block] = true;
				container_conteudo[container] = conteudo;
        
			});
	  } else {
			$(this.options.portal).removeChild($(container));
	  }
    }
    */
    
    for (var container in settings) {
	  visoes = settings[container]
	  len_visoes = visoes.length
	  if (len_visoes > 0) {
			visoes.each(function (block) {
				$(container).appendChild($(block));
				visoes_estado[block] = true;
			});
	  } else {
			$(this.options.portal).removeChild($(container));
	  }
    }

/* remove os blocks que nao foram definidos */

	for (var container in visoes_estado) {
		if (! visoes_estado[container]) {
			//get the element node
			//element = document.getElementById(container);
			//console.log(element)
			//remove the element from the document
			//document.removeChild(element);
			$(this.options.blocklist).removeChild($(container));

		}
	}


    blocks.each(
      function (block) {
        var content = Element.childrenWithClassName(
          block, this.options.content, true
        );

        var toggle = Element.childrenWithClassName(
          block, this.options.toggle, true
        );
        
        Event.observe(
          toggle, 'click', 
          function (e) { Effect.toggle(content, 'Slide'); },
          false
        );

      }.bind(this)
    );


	//portal = new Portal();
	//portal.applySettings(settings);
}
