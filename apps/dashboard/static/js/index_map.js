var map = new Datamap({
    element: document.getElementById('container'),
    fills: {
        HIGH: '#e74c3c',
        MEDIUM: '#f39c12',
        LOW: '#18bc9c',
        defaultFill: '#18bc9c'
    },
    data: {
        IRL: {
            fillKey: 'LOW',
            numberOfThings: 2002
        },
        USA: {
            fillKey: 'MEDIUM',
            numberOfThings: 10381
        }, 
        RUS: {
            fillKey:'HIGH'
        },
        MEX: {
            fillKey:'HIGH'
        },
        EGY: {
            fillKey:'HIGH'
        },
        IND: {
            fillKey:'MEDIUM'
        },
        PER: {
            fillKey:'MEDIUM'
        },
    }
});

//draw a legend for this map
map.legend();
