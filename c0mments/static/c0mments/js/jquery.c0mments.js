;(function( $ ){
    var pluginName = 'comments';
    var defaults = {
        indent_size: 20
    };
    var utils = {
        hideObject: function(obj){
            tmp = obj.clone();
            obj.remove('');
            return tmp;
        }
    };
    var methods = {
        init: function (options){
            return this.each(function(){
                var $this = $(this), data = $this.data(pluginName);
                if ( ! data ) {
                    $(this).data(pluginName, $.extend({
                        target: $this, 
                        comment_sel: $this.attr('data-comment-block')
                    }, defaults, options));
                }                
            }).comments('build');
        },
        build: function(){
            return this.each(function(){
                var $this = $(this), ds = $this.data(pluginName);
                $(ds.comment_sel).each(function(){
                    var $comment = $(this);
                    pk = $comment.attr('data-comment-pk');
                    reply_sel = $comment.attr('data-comment-reply');
                    $comment.find(reply_sel).bind('click', { pk: pk }, function(ev){
                        if (!ds.reply_form){
                            ds.reply_form = $(ds.form_sel).clone();
                            ds.reply_form.submit(function(){
                                $.ajax({
                                    type: 'POST',
                                    data: $(this).serialize(),
                                    dataType: 'JSON',
                                    success: function(data){
                                        if (typeof data.error == 'undefined'){
                                            obj = $(data.comment);
                                            $comment.after(obj);
                                            margin_left = parseInt($comment.css('margin-left').replace('px',''))+ds.indent_size;
                                            obj.css('margin-left', margin_left);
                                            // alert(data.message);
                                            ds.reply_form = utils.hideObject(ds.reply_form);
                                        }else{
                                            // alert(data.message);
                                        }
                                    }
                                });
                                return false;
                            });
                        }
                        $comment.siblings().click(function(){
                            ds.reply_form = utils.hideObject(ds.reply_form);
                            $comment.siblings().unbind('click');
                        });
                        $comment.after(ds.reply_form);
                        ds.reply_form.find('input[name="parent"]').val(ev.data.pk);
                        ds.reply_form.css('margin-left', $comment.css('margin-left'));
                    });
                });
            });
        },
        destroy : function( ) {
            return this.each(function(){
                var $this = $(this), data = $this.data(pluginName);
                $this.removeData(pluginName);
            });
        }
    };
    $.fn.comments = function( method ) {
        if ( methods[method] ) {
            return methods[method].apply( this, Array.prototype.slice.call( arguments, 1 ));
        } else if ( typeof method === 'object' || ! method ) {
            return methods.init.apply( this, arguments );
        } else {
            $.error( 'Method ' +  method + ' does not exist on jQuery.tooltip' );
        }    
    };
})( jQuery );
