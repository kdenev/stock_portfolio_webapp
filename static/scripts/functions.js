$(function () {
  $('#table').bootstrapTable()
})

// $(function () {
//   $("#sector-filter").on('click', function (e) {
//     e.preventDefault();
//     var sector = $(this).val();
//     console.log(sector)
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