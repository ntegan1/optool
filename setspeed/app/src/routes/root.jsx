import Nav from "../components/Nav"

function MobileOrNot() {
  return (
  <>
    <div className="md:hidden w-full flex flex-col items-center mt-4">
      <p
        className="text-nord5 font-bold text-2xl portait:hidden landcape:md:hidden">
        Youre on mobile
      </p>
    </div>
    <div className="md:hidden w-full flex flex-col items-center mt-4">
      <p
        className="text-nord5 font-bold text-2xl landscape:hidden">
        portrait
      </p>
      <p
        className="text-nord5 font-bold text-2xl portrait:hidden">
        landscape
      </p>
    </div>
  </>
  )
}
export default function Root() {
  return (
    <>
      <Nav />
      <MobileOrNot />
    </>
  )
}
