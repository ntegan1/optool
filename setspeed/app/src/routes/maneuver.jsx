import { useEffect, useRef, useState } from "react"
import Nav from "../components/Nav"

export default function Root() {
  return (
    <>
      <div className="h-screen w-screen">
        <Nav />
        <Sliders />
      </div>
    </>
  )
}


function Sliders() {
  const c = "[&::-webkit-slider-thumb]:bg-nord8 [&::-webkit-slider-thumb]:w-12 [&::-webkit-slider-thumb]:h-12 [&::-webkit-slider-thumb]:rounded-full [&::-webkit-slider-thumb]:[appearance:none] [&::-webkit-slider-thumb]:[-webkit-appearance:none] [-webkit-user-select:none] -translate-x-[134px] translate-y-[134px] -rotate-90 h-[32px] w-[300px] bg-gray-700 rounded-lg appearance-none cursor-pointer "
  //const url = ""
  //const url = "http://192.168.1.122:5000"
  //const url = "http://127.0.0.1:5000"
  //const url = "http://192.168.1.180:5000"
  const url = "http://192.168.8.175:5000"
  const vmin = 0
  const vmax = 28
  const amin = 0
  const amax = 200
  const amid = (amin + amax) / 2
  const sendingDelay = 200
  const waitingDelay = 1200
  const [value, setValue] = useState(vmax)
  const [valueA, setValueA] = useState(amid)
  const [serverRunning, setServerRunning] = useState(false)
  const [intervalDelay, setIntervalDelay] = useState(waitingDelay)
  const int_loop = () => { sendv(value, valueA); }
  const onclick = (e) => {setValue(vmax); setValueA(amid); sendv(vmax, amid) }
  const onreleaseA = (e) => {e.target.valueAsNumber = amid; setValueA(amid); sendv(value, amid) }
  const onchange = (e) => {const f = e.target.valueAsNumber; setValue(f); sendv(f, valueA)}
  const onchangeA = (e) => {const f = e.target.valueAsNumber; setValueA(f); sendv(value, f)}
  const [done, setDone] = useState(true)
  const sendalwaysish = (v, a) => { if (serverRunning) { sendalways(v, a) } }
  const pingServer = () => {
    try {
      fetch(url + "/ping", {cache: "no-store", mode:"cors", method: "GET", keepalive: true}).then(res => {
        setDone(true)
        if (res.status === 200) {
          setServerRunning(true)
          setIntervalDelay(sendingDelay)
        }
      }).catch((e) => {
        setDone(true)
      })
    }
    catch (e) {
      setDone(true)
    }
  }
  const sendalways = (v, a) => {
    try {
      fetch(url + "/control/" + v + "/" + a, {cache: "no-store", mode:"cors", method: "GET", keepalive: true}).then((res) => {
        if (res.status !== 200) {
          setServerRunning(false)
          setIntervalDelay(waitingDelay)
        }
        setDone(true)
      }).catch((e) => {
        setDone(true)
        setIntervalDelay(waitingDelay)
        setServerRunning(false)
      })
    }
    catch (e) {
      setServerRunning(false)
      setIntervalDelay(waitingDelay)
      setDone(true)
    }
  }
  const check_server_running = () => { console.log("no server"); pingServer() }
  const sendv = (v, a) => {
    if (!serverRunning) {
      setDone(false)
      check_server_running()
      return
    }
    // only send if done
    if (!done) { console.log("wait"); return }
    setDone(false)
    sendalways(v, a)
  }
  useInterval(int_loop, intervalDelay)
  useEffect(() => {
    sendalwaysish(vmax, amid)
    console.log("reload")
    return () => {
      sendalways(vmax, amid)
      console.log("unmount")
    }
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [])
  if (!serverRunning)
    return (
      <>
        <button className={"font-bold mt-4 w-64 h-24 rounded-3xl bg-nord11"}>
          <p className="text-nord1 text-2xl">Waiting for Server</p>
        </button>
      </>
    )
  return (
    <>
      <div className="flex justify-between mx-8 mb-2">
        <div className="h-[300px] w-[32px] mt-4">
          <input onMouseUp={onreleaseA} onTouchEnd={onreleaseA} type="range" onChange={onchangeA} value={valueA} min={amin} max={amax} className={c} />
        </div>
        <div>
          <div className="h-[300px] w-[32px] mt-4">
            <input type="range" step="1" onChange={onchange} value={value} min={vmin} max={vmax} className={c} />
          </div>
          <p className="pl-3 text-xl font-bold mt-2 text-nord5">{value} <span className="text-sm font-medium text-nord5">mph</span></p>
        </div>
      </div>
      <button onClick={onclick} className={"font-bold mt-4 w-64 h-24 rounded-3xl" + ((value === vmax) ? " bg-nord8 " : " bg-nord6 ")}>
        <p className="text-nord1 text-2xl">reset</p>
      </button>
    </>
  )
}







function useInterval(callback, delay) {
  const savedCallback = useRef();

  // Remember the latest callback.
  useEffect(() => {
    savedCallback.current = callback;
  }, [callback]);

  // Set up the interval.
  useEffect(() => {
    function tick() {
      savedCallback.current();
    }
    if (delay !== null) {
      let id = setInterval(tick, delay);
      return () => clearInterval(id);
    }
  }, [delay]);
}
