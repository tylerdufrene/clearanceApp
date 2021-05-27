$(document).ready(function() {
    $(".filter-checkbox").on('click', function(){
        var _filterObj={};
        $(".filter-checkbox").each(function(index, ele){
            var _filterVal=$(this).val();
            var _filterKey=$(this).data('filter');
            console.log(_filterKey, _filterVal)
        });
    });
});