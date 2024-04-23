$(function () {
  $('#table').bootstrapTable()
})

// $(function () {
//   $("#sector-filter").on('change', function (e) {
//     e.preventDefault();
//     var sector = $(this).val();
//     $.ajax({
//       type: "POST",
//       url: "/sector_filter",
//       data: {sector: sector},
//       success: function (result) {
//         console.log(result)
//         // $("#table").bootstrapTable(result);
//       }
//     });
//   });
// });