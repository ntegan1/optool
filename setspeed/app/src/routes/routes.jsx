import Nav from "../components/Nav"
import { useLoaderData } from "react-router-dom"
import { useState } from "react"
export async function loader() {
  const res = await fetch("/routelistv2")
  const routes = await res.json()
  return { routes }
}

function RouteVideo({routename, segment, onended, camera}) {
  const url = "/"
  return (
  <>
    <video onEnded={onended} muted autoPlay controls key={segment + camera}>
      <source key={segment + camera} src={url + camera + "/" + segment} type="video/mp4" />
    </video>
  </>
  )
}

function RouteList() {
  const onended = (e) => {
    setSegnum(s => {var a = ((s + 1) % selected.segments.length); setSegment(selected.segments[a]); return a})
  }
  const onclick = (e) => {
    const name = e.target.innerHTML
    setSelected(data.routes.list.find(f => f.name === name))
    setSegnum(0)
    setSegment(selected.segments[0]);
  }
  const data = useLoaderData()
  const [segnum, setSegnum] = useState(0)
  const [selected, setSelected] = useState(data.routes.list[segnum])
  const [segment, setSegment] = useState(selected.segments[segnum])
  const cameras = ["fcamera", "ecamera", "dcamera", "qcamera"]
  const [camera, setCamera] = useState(0)
  const nextcamera = (e) => { setCamera(c => ((c + 1) % cameras.length))}

  return (
    <div className="w-full flex flex-col items-center mt-4">
      <div className="flex flex-col overflow-y-auto max-h-32">
        {
          data.routes.list.map(route =>
            <button className="text-nord5 px-2" key={route.name} onClick={onclick}>{route.name}</button>
          )
        }
      </div>
      <span className="text-nord5">playing: {segment}</span>
      <div className="flex">
        <button onClick={onended} className="text-nord5 mr-2">nextsegment</button>
        <button onClick={nextcamera} className="text-nord5">{cameras[camera]}</button>
      </div>
      <RouteVideo routename={selected.name} segment={segment} onended={onended} camera={cameras[camera]} />
    </div>
  )
}

export default function Routes() {
  return (
    <>
      <Nav />
      <RouteList />
    </>
  )
}
