import axios from "axios"
import { Dispatch, SetStateAction } from "react"
import { Row } from "./structs"

const dataToRow = (d: any) => ({
    actual_datetime: new Date(d.actual_datetime),
    row_date: new Date(d.row_date),
    is_day: d.is_day,
    temperature: d.temperature,
})

export const getRows = async (
    setRows: Dispatch<SetStateAction<Row[]>>,
    setLoading: Dispatch<SetStateAction<boolean>>
) => {
    let endpoint = `/api/observations`
    let response = await axios.get(endpoint)
    let data = response.data
    let objects = data.map(dataToRow)
    setRows(objects)
    setTimeout(() => setLoading(false), 100)
}
