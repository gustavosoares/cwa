var Portal = Class.create();

/* obtem o posicionamento das visoes */
function obter_estado() {
	
	var colunas = $('portal').getElementsByClassName('portal-column');
	//console.log(colunas)
	var i=0;
	var colunasLen=colunas.length;
	//armazena o estado dos containers
	var postBody = "";
	for (i=0;i <= colunasLen;i++) {
		aux = colunas[i];
		if (aux != undefined) {
			aux_id = aux.id;
			if (aux_id != 'portal-column-block-list') {
				if (postBody == "") {
					postBody = aux_id
				} else{
					postBody = postBody + '&' + aux_id;
				}
				/*console.log("------")
				console.log(aux)
				console.log('id: ' + aux_id)*/
				var children = $(aux_id).getElementsByClassName('block');
				if (children.length > 0) {
					var j=0;
					//console.log(children)
					for (j=0; j <= children.length; j++) {
						if (children[j] != undefined) {
							children_id = children[j].id
							postBody = postBody + ':' + children_id
							//console.log(children_id)
						}
					}
				}
			}
		}

	}
	//console.log('postBody: '+ postBody)
	$('id_metadado').value = postBody;
	
}
Portal.prototype = {
  initialize: function (options) {
    this.setOptions(options);
    var sortables = document.getElementsByClassName(
      this.options.column, this.options.portal
    );

    //console.log(sortables)
    sortables.each(function (sortable) {
      Sortable.create(sortable, { 
        containment: sortables,
        constraint: false,
        tag: 'div',
        only: this.options.block,
        dropOnEmpty: true,
        handle: this.options.handle,
        hoverclass: this.options.hoverclass,
        onUpdate: function (container) {
			obter_estado();
        }.bind(this)
      });
    }.bind(this));
    
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

        var delete_ = Element.childrenWithClassName(
          block, 'block-delete', true
        );

        Event.observe(
          toggle, 'click', 
          function (e) { Effect.toggle(content, 'Slide'); },
          false
        );
        
        Event.observe(
          delete_, 'click', 
          function (e) {
            $('portal-column-block-list').appendChild($(block));
            obter_estado();
          },
          false
        );

      }.bind(this)
    );
    
    Event.observe(
      this.options.blocklistlink, 'click', 
      this.displayBlockList.bindAsEventListener(this), 
      false
    );

    new Draggable(this.options.blocklist, {
        scroll: window,
        handle: this.options.blocklisthandle,
      }
    );
    
  },

  displayBlockList: function (e) {
    Effect.toggle(this.options.blocklist);
    Event.stop(e);
  },

  setOptions: function (options) {
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
      saveurl: ''
    }
    Object.extend(this.options, options || {});
  },

  applySettings: function (settings) {
    for (var container in settings) {
      settings[container].each(function (block) {
        $(container).appendChild($(block));
      });
    }
  }
}

