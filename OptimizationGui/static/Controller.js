// here all the code that connect the html view to the server.

$(document).ready(
    function() {
    let array_to_send = []  // this list will have all the nurse wanted shifts
    let shift_percentage = [] //this list will have the percentage shift of each nurse
    let selected_algo = [] // the algorithm the user selected
    function CreateTable(name){
        let table = document.createElement("TABLE")  // create the table
        table.border = ""
        table.width = "50%"
        let thead = table.createTHead(); // create table head
        let row = thead.insertRow(0)
        let table_head_cells = []
        let j = 0;
        for (j = 0; j < 3; j++){
            table_head_cells[j] = row.insertCell(j)  // insert 3 cells
        }
        table_head_cells[0].innerHTML = "M"
        table_head_cells[1].innerHTML = "N"
        table_head_cells[2].innerHTML = "E"

        let tbody_row = table.insertRow(1)
        let input_cells = []
        for (j = 0; j < 3; j++){
            input_cells[j] = document.createElement("INPUT");  // insert 3 cells
            input_cells[j].setAttribute("type", "checkbox");  //make them check box cell
            input_cells[j].addEventListener("change",function () {
                let nurse = $(this).closest('table').closest('tr')[0].rowIndex - 1 // get the row of the specific checkbox
                let day = $(this).closest('table').closest('td')[0].cellIndex - 2//get the day
                let shift = $(this).closest('td')[0].cellIndex //get the shift
                let weekly_shift = array_to_send[nurse].split(" ") // get the shifts of the nurse
                let temp_shift = ""  // get the shifts of the day
                let daily_shift = "1" //this will save the value of checked/uncheckd shift
                if (this.checked) {  // the checkbox is checked
                    daily_shift = "0" //the nurse wants the shift
                }

                //run on all the shifts of the day and replace the desired shift
                weekly_shift[day].split('').forEach(function (val, index) {
                    if (index === shift){
                        temp_shift += daily_shift
                    }else {
                        temp_shift += val
                    }
                })
                weekly_shift[day] = temp_shift
                array_to_send[nurse] = weekly_shift.join(' ')  // update the shifts of the nurse
            })
            tbody_row.insertCell(j).appendChild(input_cells[j])
        }
        return table; // return the table
    }

    function create_new_nurse() {  //this function create a new nurse
        array_to_send.push("111 111 111 111 111 111 111")  //insert a new nurse schedual
        // here we will add a new row for the nurse table
        let nurse_table = document.getElementById("nurse_table_body")  //get the body of the nurse table
        // the row
        let row = nurse_table.insertRow(nurse_table.rows.length)  // insert the nurse to the last row

        let i = 0;  // will be the counter for the loops

        // build the input for nurse name and shift percentage
        let input_cell = []
        input_cell[0] = document.createElement("INPUT");
        input_cell[0].setAttribute("type", "text");
        input_cell[1] = document.createElement("INPUT");
        input_cell[1].setAttribute("type", "text");

        // define each cell
        let cells = [];
        for (i = 0; i < 9; i++) {
            cells[i] = row.insertCell(i);
            if (i === 0 || i === 1) {
                cells[i].appendChild(input_cell[i])
            } else {
                cells[i].appendChild(CreateTable())
            }
        }
        return row;
    }

    //this function return the nurses names
    function get_nurse_names() {
        let names = []
        for (let row of document.getElementById("nurse_table_body").rows) {
            names.push(row.cells[0].children[0].value)  // get the nurses name
        }
        return names
    }

    //build the output table
    function build_result_table(shifts) {
        //check if there is a solution
        let shifts_dic = {"0":"M", "1":"N", "2":"E"}
        let days_dic = {"1": "ST", "2":"MT", "3":"TT", "4":"WT", "5":"ThT", "6":"FT", "7":"SaT"}
        Object.keys(shifts_dic).forEach(function (shift_key_val) {
            Object.keys(days_dic).forEach(function (day_key) {
                $("#" + shifts_dic[shift_key_val] + days_dic[day_key]).empty() // clear the tables
            })
        })
        if (shifts[0] !== "there is no solution!") {
            let names = get_nurse_names() // get the nurses names
            let day = ""
            shifts.forEach(function (nurse_shift, index) {
                // nurse shift is a string
                nurse_shift = nurse_shift.trim() // remove trailing spaces
                if (nurse_shift === ""){  // ignore empty values
                    return;
                }
                let split_n = nurse_shift.split(" ") // split the line according to space
                if (split_n[0] === "Day"){
                    day = split_n[1]  // get the day
                } else {
                    //get the correct table
                    let table = document.getElementById(shifts_dic[split_n[4]] + days_dic[day])
                    let row = table.insertRow(table.rows.length)  // insert a new row
                    let x = document.createElement("LABEL");  // create a label
                    x.innerHTML = names[split_n[1]]  // take the nurse name
                    let cell = row.insertCell(0)
                    cell.appendChild(x);
                    if (split_n.length === 5) { // green from requested and red for not
                        cell.style.background = "green"
                    } else {
                        cell.style.background = "red"
                    }
                }
            })
        }
    }


    //parse the return data and save in global variable
    function GetData(result) {
        $.ajax({
            type: 'GET',
            contentType: 'application/json',
            url: '/get_data',
            dataType: 'json',
            success: function (result) {
                present_data(result)
            }, error: function (result) {
                present_data(result)
            }
        });
        $("#result_div").slideDown("slow");
        $("#image_div").slideDown("slow");
        // check if the algorithem is one of this and present the plot
        if (selected_algo[0] === "simulated_annealing" || selected_algo[0] === "genetic" ||
            selected_algo[0] === "hill_climbing" || selected_algo[0] === "random_restart") {
            let d = new Date()
            $("#graph_image").attr("src", "/static/OptimizationGui.png?"+d.getTime());
            let img = document.getElementById("graph_image");
            img.style.display = "flex"; // forget from the image
        }
        document.getElementById("backdrop").style.visibility = "hidden"
        document.getElementById("curtain").style.visibility = "visible"
        // take the result shifts with out spaces
        build_result_table(result)
    }

    // show the data to the screen
    function present_data(data){
        if (data.status === 200) {
            document.getElementById("backdrop").style.visibility = "hidden"
            document.getElementById("curtain").style.visibility = "visible"
            $("#curtain").html(data.responseText);
        }
    }


    document.getElementById("start").addEventListener("click",function () {
        if (array_to_send.length === 0){
            alert("Please Insert Nurse Input")
            return;
        }
        shift_percentage = []  // erase the previous shift percentage
        for (let row of document.getElementById("nurse_table_body").rows) {
            if (row.cells[1].children[0].value === "") {
                alert("Please enter percentage shift for each nurse")
                return
            } else {
                shift_percentage.push(row.cells[1].children[0].value)
            }
        }
        if (selected_algo.length === 0) {
            alert("Please Select Algorithm!")
            return;
        }
        if ($("#" + selected_algo[0] + "_txt").length) {  // if exist take the value
            let algo_parameter = document.getElementById(selected_algo[0] + "_txt").value // taking the value of the algo param
            if (algo_parameter === "") {
                alert("Please define the algorithm parameter!")
                return;
            } else {
                if (selected_algo.length === 2) {
                    let algo_name = selected_algo[0]
                    selected_algo = []
                    selected_algo.push(algo_name)
                }
                selected_algo.push(algo_parameter)  // enter the algo parameter
            }
        }
        let data = []  // this is the array that we will send to the server
        data.push(array_to_send)
        data.push(shift_percentage)
        data.push(selected_algo)
        $.ajax({
            type: 'POST',
            contentType: 'application/json',
            url: '/user_data',
            dataType: 'json',
            data: JSON.stringify(data),
            success: function (result) {
                GetData(result);
            }, error: function (result) {
                GetData(result);
            }
        });

    })

    document.getElementById("insert_new_nurse").addEventListener("click",create_new_nurse)

    document.getElementById("generate_random").addEventListener("click",function () {
        array_to_send = []  // erase all the previous shifts
        // generate random nurses
        let num_nurse = parseInt(document.getElementById("num_nurse").value)  // take the value from the text box
        // check valid
        if (isNaN(num_nurse)){
            alert("please enter number!")
            return
        } else if (num_nurse < 0){
            alert("please enter positive number!")
            return;
        }
        $("#nurse_table_body").empty() // clean the table rows
        let nurse_num = num_nurse
        while(num_nurse > 0){
            let row = create_new_nurse()
            let i = 0;
            let j = 0;
            for(i = 0; i < row.cells.length;i++){
                if (row.cells[i].children[0].tagName === "TABLE"){
                    let table = row.cells[i].children[0] // get the table
                    for (j = 0; j < table.rows[1].cells.length; j++){
                        if (Math.random() >= 0.5){ // with probability of 0.5 we will check the check box
                            table.rows[1].cells[j].children[0].checked = true
                            table.rows[1].cells[j].children[0].dispatchEvent(new Event("change"))
                        }
                    }
                } else {
                    if (i !== 1) {
                        row.cells[i].children[0].value = "Nurse" + (nurse_num - num_nurse + 1).toString()  // enter the nurse name
                    } else {
                        row.cells[i].children[0].value = Math.floor(Math.random() * 4) + 2  // enter shift percentage
                    }
                }
            }
            num_nurse = num_nurse - 1;
        }
    })

    let check_box_ids = ["shift_min","simulated_annealing","genetic","random_restart", "hill_climbing", "csp", "MaxShifts"]  // all the ids of the algorithms checkbox
    let check_box_item = []
    check_box_ids.forEach(function (check_box_id) {
        let c_item = document.getElementById(check_box_id)
        c_item.addEventListener("change",function () {
            let item_change = this
            if (selected_algo.length > 0) {
                selected_algo = []  // create a new array
            }
            if (item_change.checked) {
                if ($("#" + item_change.id + "_div").length) {  // if exist make it visible
                    $("#" + item_change.id + "_div").slideDown("slow");
                }
                selected_algo.push(item_change.id) // get the name of the algorithm
                check_box_item.forEach(function (item_value) {
                    if (item_change !== item_value) {
                        if (item_value.checked) {
                            item_value.checked = false;
                        }
                        if ($("#" + item_value.id + "_div").length) {  // if exist erase the value
                            let txt_input = document.getElementById(item_value.id + "_txt")
                            txt_input.value = ""
                            $("#" + item_value.id + "_div").slideUp("slow");
                        }
                    }
                })
            } else {
                if ($("#" + item_change.id + "_txt").length) {  // if exist make it hidden
                    $("#" + item_change.id + "_div").slideUp("slow");
                }
            }
        })
        check_box_item.push(c_item)  // get the element and insert to check box item list
    })


})