import Nav from "../components/Nav"

export default function Root() {
  const c = "[&::-webkit-slider-thumb]:bg-nord8 [&::-webkit-slider-thumb]:w-12 [&::-webkit-slider-thumb]:h-12 [&::-webkit-slider-thumb]:rounded-full [&::-webkit-slider-thumb]:[appearance:none] [&::-webkit-slider-thumb]:[-webkit-appearance:none] [-webkit-user-select:none] -translate-x-[134px] translate-y-[134px] -rotate-90 h-[32px] w-[300px] bg-gray-700 rounded-lg appearance-none cursor-pointer "

  const f = (e) => {
    e.target.valueAsNumber = 0
  }
  return (
    <>
      <div className="h-screen w-screen">
        <Nav />
        <div className="flex justify-between mx-4">
        <div className="h-[300px] w-[32px] mt-4">
          <input onMouseUp={f} onTouchEnd={f} type="range" defaultValue="0" min="-100" max="100" className={c} />
        </div>
        <div className="h-[300px] w-[32px] mt-4">
          <input type="range" step="1" defaultValue={28} min={0} max={28} className={c} />
        </div>
        </div>
      </div>
    </>
  )
}
