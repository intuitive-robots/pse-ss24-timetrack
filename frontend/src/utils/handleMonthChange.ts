export const handleMonthChange = (
  direction: string,
  month: number,
  year: number,
  setMonth: (month: number) => void,
  setYear: (year: number) => void
) => {
  let newMonth = month;
  let newYear = year;

  if (direction === 'next') {
    if (month === 12) {
      newMonth = 1;
      newYear += 1;
    } else {
      newMonth += 1;
    }
  } else if (direction === 'prev') {
    if (month === 1) {
      newMonth = 12;
      newYear -= 1;
    } else {
      newMonth -= 1;
    }
  }

  localStorage.setItem('selectedMonth', newMonth.toString());
  localStorage.setItem('selectedYear', newYear.toString());

  setMonth(newMonth);
  setYear(newYear);
};