function tabulatorResStats(result) {
    // Takes data from the ajax call made when you open a reservoir page
    // Filters out the data from the result with the statistics information
    // Creates the statistics tabulator page

    var overviewTable = new Tabulator("#overview-table", {
        data:result,              //load row data from array
        layout:"fitColumns",      //fit columns to width of table
        responsiveLayout:"hide",  //hide columns that dont fit on the table
        tooltips:true,            //show tool tips on cells
        addRowPos:"top",          //when adding a new row, add it to the top of the table
        history:true,             //allow undo and redo actions on the table
        pagination:"local",       //paginate the data
        paginationSize:10,        //allow 7 rows per page of data
        movableColumns:false,     //allow column order to be changed
        resizableRows:true,       //allow row order to be changed
        initialSort:[             //set the initial sort order of the data
            {column:"name", dir:"asc"}
        ],
        columns:[                 //define the table columns
            {title:"Nombre", field:"name", editor:false},
            {title:"Nivel MÁXIMO", field:"maxlvl", align:"center"},
            {title:"Nivel ACTUAL", field:"actlvl", align:"center"},
            {title:"Nivel MÍNIMO", field:"minlvl", align:"center"},
            {title:"Volumen MÁXIMO", field:"maxvol", align:"center"},
            {title:"Volumen ACTUAL", field:"actvol", align:"center"},
            {title:"Volumen UTIL", field:"utilvol", align:"center"},
            {title:"Volumen MÍNIMO", field:"minvol", align:"center"},
        ]
    });
}


function tabulatorOutflows(result) {

    var unitOpts = {
        'mcs': 'Metros Cubicos Segundo',
        'cfs': 'Cubic Feet per Second'
    };

    return outflowtable = new Tabulator("#outflowTable", {
        data:result,                //load row data from array
        layout:"fitColumns",      //fit columns to width of table
        responsiveLayout:"hide",  //hide columns that dont fit on the table
        tooltips:true,            //show tool tips on cells
        addRowPos:"top",          //when adding a new row, add it to the top of the table
        history:true,             //allow undo and redo actions on the table
        pagination:"local",       //paginate the data
        paginationSize:10,        //allow 7 rows per page of data
        movableColumns:false,     //allow column order to be changed
        resizableRows:true,       //allow row order to be changed
        initialSort:[             //set the initial sort order of the data
            {column:"date", dir:"asc"}
        ],
        columns:[                 //define the table columns
            {title:"Fecha", field:"date", formatter:"datetime", editor:false, formatterParams:{inputFormat:"MM-DD-YYYY", outputFormat:"DD/MM/YY"}},
            {title:"Entradas (pronosticadas)", field:"inflow", align:"center"},
            {title:"Caudales de Salida", field:"release", align:"center", formatter:"plaintext", editor:true},
            {title:"Unidades", field:"units", align:"center", editor:"select", editorParams:unitOpts},
            {title:"Tiempo de Salida (Horas)", field:"time", align:"center", formatter:"plaintext", editor:true}
        ]
    });
}