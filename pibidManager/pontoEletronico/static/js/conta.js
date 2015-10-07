function removeObrigatoriedade() {

    var campo = new Array('favorecido_id', 'documento_conta_id', 'data_vencimento',
            'valor', 'plano_conta_id', 'centro_custo_id');

    var i;
    for (i in campo) {
        $('#' + campo[i]).removeAttr('required');
    }
}

function carregaConfiguracao(){
    removeObrigatoriedade();
    $('#acao').val('carregar_configuracao');
    $('#form').submit();
}