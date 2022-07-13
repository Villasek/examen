$('#Usuario').validate({ 
    "rules": {
        "Cantidad": {
            required: true,
        },
    },
    messages: {
        "Cantidad": {
            required: 'Debe llenar este campo',
        },
    }
});

$('#Contraseña').validate({ 
    "rules": {
        "Cantidad": {
            required: true,
        },
    },
    messages: {
        "Cantidad": {
            required: 'Debe llenar este campo',
        },
    }
});

