import { useEffect, useRef, useState } from "react"
import Nav from "./components/Nav"
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

function Slider() {
  const url = ""
  //const url = "http://192.168.1.122:5000"
  const vmin = 0
  const vmax = 28
  const sendingDelay = 200
  const waitingDelay = 1200
  const [value, setValue] = useState(vmax)
  const [serverRunning, setServerRunning] = useState(false)
  const [intervalDelay, setIntervalDelay] = useState(waitingDelay)
  const int_loop = () => { sendv(value); }
  const onclick = (e) => {setValue(vmax); sendv(vmax) }
  const onchange = (e) => {const f = e.target.valueAsNumber; setValue(f); sendv(f)}
  const [done, setDone] = useState(true)
  const sendalwaysish = (v) => {
    if (!serverRunning) {
      return
    }
    sendalways(v)
  }
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
  const sendalways = (v) => {
    try {
      fetch(url + "/control/" + v, {cache: "no-store", mode:"cors", method: "GET", keepalive: true}).then((res) => {
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
  const check_server_running = () => {
    console.log("no server")
    pingServer()
  }
  const sendv = (v) => {
    if (!serverRunning) {
      setDone(false)
      check_server_running()
      return
    }
    // only send if done
    if (!done) { console.log("wait"); return }
    setDone(false)
    sendalways(v)
  }
  const c = "[&::-webkit-slider-thumb]:bg-nord8 [&::-webkit-slider-thumb]:w-12 [&::-webkit-slider-thumb]:h-12 [&::-webkit-slider-thumb]:rounded-full [&::-webkit-slider-thumb]:[appearance:none] [&::-webkit-slider-thumb]:[-webkit-appearance:none] [-webkit-user-select:none] -translate-x-[134px] translate-y-[134px] -rotate-90 h-[32px] w-[300px] bg-gray-700 rounded-lg appearance-none cursor-pointer "
  useInterval(int_loop, intervalDelay)
  useEffect(() => {
    sendalwaysish(vmax)
    console.log("reload")
    return () => {
      sendalways(vmax)
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
      <div className="h-[300px] w-[32px] mt-4">
        <input type="range" step="1" onChange={onchange} value={value} min={vmin} max={vmax} className={c} />
      </div>
      <p className="text-xl font-bold mt-2">{value}</p>
      <button onClick={onclick} className={"font-bold mt-4 w-64 h-24 rounded-3xl" + ((value === vmax) ? " bg-nord8 " : " bg-nord6 ")}>
        <p className="text-nord1 text-2xl">reset</p>
      </button>
    </>
  )
}
function App() {
  const title = "manual set speed"
  return (
  <>
    <Nav />
    <div className="text-nord5 w-full mt-3 flex flex-col items-center justify-between">
      <h1 className="text-4xl">{title}</h1>
      <div className="flex flex-col items-center">
        <p>slider</p>
        <Slider />
      </div>
    </div>
  </>
  );
}

export default App;
