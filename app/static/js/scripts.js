$(function () {

    $("#tabs").tabs();

});

/**********Drug Search Search********/
var drugSearchTerm = null;
function search_drug(value) {
    if (drugSearchTerm != null) drugSearchTerm.abort();
    if (value.length >= 3) {
        $("#intialDrugList").dataTable().fnClearTable(true);
        drugSearchTerm = $.ajax({
            url: "http://172.16.14.202:5000" + "/admin/product/drug_search_list",
            data: {'searchTerm': value},
            success: function (data) {
                resultTable = "";
                $.map(data, function (obj, i) {
                    var _href = obj.generic ? "prescribe-drug" : "prescribe-drug";
                    var drug_type = obj.generic ? "Generic Drug" : "Trade Name Drug";
                    var link = "<a href='"+_href+".html?drugid="+obj.id+"&prescriptionId="+prescriptionId+"'>prescribe drug</a>";
                    var name = "<a href='"+_href+".html?drugid="+obj.id+"&prescriptionId="+prescriptionId+"'>"+obj.name+"</a>";
                    $("#intialDrugList").dataTable().fnAddData([drug_type,name, link]);
                });
            }
        });
    } else {
        $("#intialDrugList").dataTable().fnClearTable(true);
    }
}
/**********End Drug Search********/