/*Funcao para adicionar o efeito do slide nos boxes*/
function init() {
	
	var widgets = document.getElementsByClassName('block', 'portal');
	var visoes_estado = {};
	widgets.each(
      function (widget) {
			widget_id = widget.id;
			visoes_estado[widget_id] = false;
      }.bind(this)
    );

	var container_conteudo = {}
	var containers = document.getElementsByClassName('portal-column');
	containers.each(
	  function (container) {
			container_id = container.id;
			if (container_id != 'portal-column-block-list') {
				container_conteudo[container_id] = '';
			}
	  }.bind(this)
	);

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

    /*
    Ex.:
    var settings = {"portal-column-1": ["block-tabular"], "portal-column-0": [], "portal-column-bottom": ["block-relatorio"]
    */
	for (var container in settings) { /* for nas chaves do settings */
	  visoes = settings[container]
	  len_visoes = visoes.length
	  if (len_visoes > 0) {
			visoes.each(function (block) {
				c = document.getElementById(container)
				conteudo = container_conteudo[container];
				conteudo = conteudo + '<div class="block" id="' + block + '">\n';
				conteudo = conteudo + $(block).innerHTML;
				conteudo = conteudo + '</div>'
				//console.log(conteudo)
				c.innerHTML = conteudo;
				//console.log(container+' -> '+block)     
				visoes_estado[block] = true;
				container_conteudo[container] = conteudo;
        
            var blocks = document.getElementsByClassName(
		      this.options.block, this.options.portal
		    );

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

        
			});
	  } else {
			$(this.options.portal).removeChild($(container));
	  }
    }

    
    /*
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
    }*/

    /* remove os blocks que nao foram definidos */
	for (var container in visoes_estado) {
		if (! visoes_estado[container]) {
			$(this.options.blocklist).removeChild($(container));
			$("id-menu").removeChild($("id-menu-"+container));
		}
	}

    var blocks = document.getElementsByClassName(
      this.options.block, this.options.portal
    );

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

}
