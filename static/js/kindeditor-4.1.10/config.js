/**
 * Created by lenovo on 2017/9/11.
 */
KindEditor.ready(function(K) {
            window.editor = K.create('textarea[name=content]',{
                width:'800px',
                heigh:'200px',
                uploadJson: '/admin/upload/kindeditor',
            });
    });
