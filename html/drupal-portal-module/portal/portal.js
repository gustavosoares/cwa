var Portal = Class.create();
Portal.prototype = {
  initialize: function (options) {
    this.setOptions(options);
    var sortables = document.getElementsByClassName(
      this.options.column, this.options.portal
    );
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
          if (!this.options.saveurl) {
            return;
          }
          if (container.id == this.options.blocklist) {
            return;
          }
          var url = this.options.saveurl;
          var postBody = container.id + ':';
          var blocks = document.getElementsByClassName(
            this.options.block, container
          );
          postBody += blocks.pluck('id').join(',');
          postBody = 'value=' + escape(postBody);
          
          new Ajax.Request(url, {
              method: 'post',
              postBody: postBody
            }
          );
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
        Event.observe(
          toggle, 'click', 
          function (e) { Effect.toggle(content, 'Slide'); },
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
        handle: this.options.blocklisthandle
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

