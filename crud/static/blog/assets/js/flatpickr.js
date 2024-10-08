flatpickr("#basic-datepicker"),
  flatpickr("#datetime-datepicker", {
    enableTime: !0,
    dateFormat: "Y-m-d H:i",
  }),
  flatpickr("#humanfd-datepicker", {
    altInput: !0,
    altFormat: "F j, Y",
    dateFormat: "Y-m-d",
  }),
  flatpickr("#minmax-datepicker", { minDate: "2020-01", maxDate: "2020-03" }),
  flatpickr("#disable-datepicker", {
    onReady: function () {
      this.jumpToDate("2025-01");
    },
    disable: ["2025-01-10", "2025-01-21", "2025-01-30", new Date(2025, 4, 9)],
    dateFormat: "Y-m-d",
  }),
  flatpickr("#multiple-datepicker", { mode: "multiple", dateFormat: "Y-m-d" }),
  flatpickr("#conjunction-datepicker", {
    mode: "multiple",
    dateFormat: "Y-m-d",
    conjunction: " :: ",
  }),
  flatpickr("#range-datepicker", { mode: "range" }),
  flatpickr("#inline-datepicker", { inline: !0 }),
  flatpickr("#basic-timepicker", {
    enableTime: !0,
    noCalendar: !0,
    dateFormat: "H:i",
  }),
  flatpickr("#fullhours-timepicker", {
    enableTime: !0,
    noCalendar: !0,
    dateFormat: "H:i",
    time_24hr: !0,
  }),
  flatpickr("#minmax-timepicker", {
    enableTime: !0,
    noCalendar: !0,
    dateFormat: "H:i",
    minDate: "16:00",
    maxDate: "22:30",
  }),
  flatpickr("#preloading-timepicker", {
    enableTime: !0,
    noCalendar: !0,
    dateFormat: "H:i",
    defaultDate: "01:45",
  });
