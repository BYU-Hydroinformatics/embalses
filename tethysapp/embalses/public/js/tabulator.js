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
            {title:"Nivel MAXIMO", field:"maxlvl", align:"center"},
            {title:"Nivel ACTUAL", field:"actlvl", align:"center"},
            {title:"Nivel MINIMO", field:"minlvl", align:"center"},
            // {title:"Promedio Anual", field:"yrAvg", align:"left", formatter:"progress", editor:true},
            // {title:"Volumen ACTUAL", field:"volAct", width:130, editor:"input"},
            // {title:"Volumen UTIL", field:"volUtil", align:"center"}
        ]
    });
}


function tabulatorOutflows() {
    // Takes data from the ajax call made when you open a reservoir page
    // Filters out the data from the result with the statistics information
    // Creates the statistics tabulator page

    var data =[]

    var outflowtable = new Tabulator("#outflowTable", {
        data:data,              //load row data from array
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
            {title:"Nivel MAXIMO", field:"maxlvl", align:"center"},
            {title:"Nivel ACTUAL", field:"actlvl", align:"center"},
            {title:"Nivel MINIMO", field:"minlvl", align:"center"},
            // {title:"Promedio Anual", field:"yrAvg", align:"left", formatter:"progress", editor:true},
            // {title:"Volumen ACTUAL", field:"volAct", width:130, editor:"input"},
            // {title:"Volumen UTIL", field:"volUtil", align:"center"}
        ]
    });
}