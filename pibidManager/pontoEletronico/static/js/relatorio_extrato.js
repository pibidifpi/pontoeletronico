function verificaOpcao(valor){
    switch(valor){
        case '6':
            $('#div-datas').slideDown();
            break;
        default:
            $('#div-datas').slideUp();
            break;

    }
}