export const getRowDateString = (row: Row) => {
    let rowDate = row.row_date
    console.log(rowDate)
    let year = rowDate.getFullYear().toString().padStart(4, "0")
    let month = (rowDate.getMonth() + 1).toString().padStart(2, "0")
    let date = rowDate.getDate().toString().padStart(2, "0")
    return `${year}-${month}-${date}`
}

export interface Row {
    actual_datetime: Date
    row_date: Date
    is_day: boolean
    temperature: number
}
