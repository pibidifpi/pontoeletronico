function calculaValor(frequencia_valor_previsto, valor_previsto){
    var valor_calculado = 0;

    switch(frequencia_valor_previsto){
        case '1': 
            //diariamente
            valor_calculado = valor_previsto * 30;
        break;
        case '2': 
            //semanalmente
            valor_calculado = valor_previsto * 4;
        break;
        case '3': 
            //mensal
            valor_calculado = valor_previsto;
        break;
        case '4':
            //anual
            valor_calculado = valor_previsto / 12;
        break;
    }

    return valor_calculado.toFixed(2);
}

function atualizaPersonalizado(){
    
    $('#frequencia_valor_previsto').val(5);
    
    var campo = new Array('valor_jan', 'valor_fev', 'valor_mar',
            'valor_abr', 'valor_mai', 'valor_jun',
            'valor_jul', 'valor_ago', 'valor_set',
            'valor_out', 'valor_nov', 'valor_dez');

    var i;
    var total_previsto = 0;
    for (i in campo) {
        var valor_previsto = parseFloat($('#' + campo[i]).val());
        
        if(isNaN(valor_previsto)){
            valor_previsto = 0;
        }
        
        total_previsto += valor_previsto;
    }
    
    $('#valor_previsto').val(total_previsto.toFixed(2));
} 

function setaValor(valor_calculado){
    var campo = new Array('valor_jan', 'valor_fev', 'valor_mar',
            'valor_abr', 'valor_mai', 'valor_jun',
            'valor_jul', 'valor_ago', 'valor_set',
            'valor_out', 'valor_nov', 'valor_dez');

    var i;
    for (i in campo) {
        $('#' + campo[i]).val(valor_calculado);
    }
} 

function atualizarValor(){
    var valor_previsto = parseFloat($('#valor_previsto').val());
    var frequencia_valor_previsto = $('#frequencia_valor_previsto').val();

    if(isNaN(valor_previsto)){
        alert('Informe um Valor Previsto válido! ');
        return null;
    }

    if(frequencia_valor_previsto === '5'){
        //personalizado
        atualizaPersonalizado();
        
    }else{
        var valor_calculado = calculaValor(frequencia_valor_previsto, valor_previsto);
        setaValor(valor_calculado);
        
    }
    
}         