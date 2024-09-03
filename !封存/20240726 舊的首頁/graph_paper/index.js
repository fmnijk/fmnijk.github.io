function add_grid() {
    var grids_count = document.getElementById("grids_count")
    grids_count.value = Number(grids_count.value) + 1

    var str =
        "<table id='table_1'>\
            <tr>\
                <td><label>Line Color (RGBA)</label></td>\
                <td class='rgba'>\
                    <input id='r_1' class='r' type='text' value='0' />\
                    <input id='g_1' class='g' type='text' value='0' />\
                    <input id='b_1' class='b' type='text' value='0' />\
                    <input id='a_1' class='a' type='text' value='255' />\
                </td>\
            </tr>\
            <tr>\
                <td><label>Line Width (px)</label></td>\
                <td><input id='line_width_1' type='text' value='!' /></td>\
            </tr>\
            <tr>\
                <td><label>Grid Cell Size (px)</label></td>\
                <td><input id='cell_size_1' type='text' value='?' /></td>\
            </tr>\
        </table>"
    str = str.replaceAll("1", grids_count.value)
    str = str.replaceAll("!", grids_count.value)
    if (Number(grids_count.value) <= 2) {
        str = str.replaceAll("?", 5 * Math.pow(5, Number(grids_count.value)))
    }
    else {
        str = str.replaceAll("?", 125 * Math.pow(2, Number(grids_count.value) - 2))
    }

    var div = document.getElementById("grids")
    div.insertAdjacentHTML("beforeend", str)
}

function remove_grid() {
    var grids_count = document.getElementById("grids_count")
    if (Number(grids_count.value) > 0) {
        var div = document.getElementById("table_" + grids_count.value)
        grids_count.value = Number(grids_count.value) - 1
        div.remove()
    }
}

function generate() {
    var grids_count = document.getElementById("grids_count")
    var canvas = document.createElement("canvas")
    canvas.width = document.getElementById("paper_width").value
    canvas.height = document.getElementById("paper_height").value

    var r = document.getElementById("r").value
    var g = document.getElementById("g").value
    var b = document.getElementById("b").value
    var a = document.getElementById("a").value
    var ctx = canvas.getContext('2d')
    ctx.fillStyle = "rgba(" + r + "," + g + "," + b + "," + a + ")"
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    for (var i = 1; i <= Number(grids_count.value); i++) {
        var cell_size = document.getElementById("cell_size_" + i).value
        ctx.lineWidth = document.getElementById("line_width_" + i).value
        r = document.getElementById("r_" + i).value
        g = document.getElementById("g_" + i).value
        b = document.getElementById("b_" + i).value
        a = document.getElementById("a_" + i).value
        ctx.strokeStyle = "rgba(" + r + "," + g + "," + b + "," + a + ")"

        ctx.beginPath()
        for (var j = 0; j <= canvas.width; j += Number(cell_size)) {
            ctx.moveTo(j, 0)
            ctx.lineTo(j, canvas.height)
        }
        for (var j = 0; j <= canvas.height; j += Number(cell_size)) {
            ctx.moveTo(0, j)
            ctx.lineTo(canvas.width, j)
        }
        ctx.stroke()
    }

    var link = document.createElement("a")
    link.download = "graph_paper.png"
    link.href = canvas.toDataURL()
    link.click()
}