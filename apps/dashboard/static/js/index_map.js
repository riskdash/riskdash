var map = new Datamap({
    element: document.getElementById('container'),
    fills: {
        HIGH: 'red',
        LOW: 'green',
        MEDIUM: 'yellow',
        defaultFill: 'green'
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
        IND: {
            fillKey:'MEDIUM'
        },
    }
});

//draw a legend for this map
map.legend();
