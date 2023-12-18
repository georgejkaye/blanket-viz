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

export interface Colour {
    name: string
    code: string
}
export const minValue = -14
export const rangeWidth = 5
export const defaultColour = { name: "Unknown", code: "bg-[#ffffff]" }
export type ColourMap = Map<number, Colour>

export const getColour = (value: number, map: ColourMap) => {
    let roundedValue = Math.round(value)
    let offsetValue = roundedValue - minValue
    let rangeBase = Math.floor(offsetValue / rangeWidth)
    let colour = map.get(rangeBase)
    return colour ? colour : defaultColour
}

const icyBlue = {
    name: "Icy Blue",
    code: "bg-[#9db6ba]",
}
const cornflower = {
    name: "Cornflower",
    code: "bg-[#98b0d6]",
}
const aqua = {
    name: "Aqua",
    code: "bg-[#1ab7e2]",
}
const turkishBlue = {
    name: "Turkish Blue",
    code: "bg-[#7bb3ad]",
}
const emerald = {
    name: "Emerald",
    code: "bg-[#0e935a]",
}
const pastelGreen = {
    name: "Pastel Green",
    code: "bg-[#b3ebcd]",
}
const pastelYellow = {
    name: "Pastel Yellow",
    code: "bg-[#f7efc8]",
}
const sunflower = {
    name: "Sunflower",
    code: "bg-[#efc131]",
}
const orange = {
    name: "Orange",
    code: "bg-[#f76629]",
}
const pumpkin = {
    name: "Pumpkin",
    code: "bg-[#fb5630]",
}
export const defaultColourMap = new Map([
    [0, icyBlue],
    [1, cornflower],
    [2, aqua],
    [3, turkishBlue],
    [4, emerald],
    [5, pastelGreen],
    [6, pastelYellow],
    [7, sunflower],
    [8, orange],
    [9, pumpkin],
])
