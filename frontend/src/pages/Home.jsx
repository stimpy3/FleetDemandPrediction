import { useState,useEffect } from 'react'
import axios from "axios";
import {
  BarChart, Bar, XAxis, YAxis, Tooltip, CartesianGrid
} from "recharts";


const Home=()=>{
  const [day, setDay] = useState("Monday");
  const [weather, setWeather] = useState("Clear");
  const [traffic, setTraffic] = useState("Low");
  const [vehicle, setVehicle] = useState("Scooter");
  const [avgPrepTime, setAvgPrepTime] = useState(20);
  const [chartData, setChartData] = useState([]);



 useEffect(() => {
  const fetchPrediction = async () => {
    try {
      const res = await axios.post(
        "http://localhost:5000/predict-hourly",
        {
          Day_of_Week: day,
          Weather: weather,
          Traffic_Level: traffic,
          Vehicle_Type: vehicle,
          avg_prep_time: avgPrepTime
        }
      );

      setChartData(res.data);
    } catch (err) {
      console.error("Prediction API error:", err);
    }
  };

  // fetchPrediction();
}, [day, weather, traffic, vehicle, avgPrepTime]);


   return(
       <div name="container" className="relative flex max-w-[100vw] min-h-[100vh] h-fit">
            
            <section
              name="sidebar-input-container"
              className="h-[100vh] w-[200px] fixed p-[15px] z-[10]"
            >
              <div className="h-full w-full bg-[#fafafa84] backdrop-blur-[10px] rounded-lg p-3 flex flex-col gap-4">
            
                {/* Day */}
                <div className="flex flex-col gap-1">
                  <label className="text-xs font-medium text-gray-700">Day</label>
                  <select value={day}onChange={e => setDay(e.target.value)} className="rounded-md border px-2 py-1 text-sm">
                    <option>Monday</option>
                    <option>Tuesday</option>
                    <option>Wednesday</option>
                    <option>Thursday</option>
                    <option>Friday</option>
                    <option>Saturday</option>
                    <option>Sunday</option>
                  </select>
                </div>
            
                {/* Weather */}
                <div className="flex flex-col gap-1">
                  <label className="text-xs font-medium text-gray-700">Weather</label>
                  <select value={weather} onChange={e => setWeather(e.target.value)}  className="rounded-md border px-2 py-1 text-sm">
                    <option>Clear</option>
                    <option>Rainy</option>
                  </select>
                </div>
            
                {/* Traffic */}
                <div className="flex flex-col gap-1">
                  <label className="text-xs font-medium text-gray-700">Traffic</label>
                  <select value={traffic} onChange={e => setTraffic(e.target.value)}  className="rounded-md border px-2 py-1 text-sm">
                    <option>Low</option>
                    <option>Medium</option>
                    <option>High</option>
                  </select>
                </div>
            
                {/* Vehicle */}
                <div className="flex flex-col gap-1">
                  <label className="text-xs font-medium text-gray-700">Vehicle</label>
                  <select value={vehicle} onChange={e => setVehicle(e.target.value)}  className="rounded-md border px-2 py-1 text-sm">
                    <option>Bike</option>
                    <option>Scooter</option>
                  </select>
                </div>
            
               {/* Avg Prep Time */}
                <div className="flex flex-col gap-2">
                  <label value={avgPrepTime} onChange={e => setAvgPrepTime(e.target.value)}  className="text-xs font-medium text-gray-700">
                    Avg Prep Time (min)
                  </label>
                  <input
                    type="range"
                    min="5"
                    max="45"
                    step="5"
                    value={avgPrepTime}
                    onChange={(e) => setAvgPrepTime(Number(e.target.value))}
                    className="w-full"
                  />
                  <span className="text-xs text-gray-500 text-right">{avgPrepTime} min</span>
                </div>
            
              </div>
            </section>
{/*  */}

            <article name="dashboardBody" className="relative pl-[200px] bg-gradient-to-tl from-[#d5afe3] to-[#f3d9c9] w-[100%] min-h-[100vh] flex max-h-fit p-[15px] overflow-hidden flex-col bg-wite">
                
                <div className="h-[50px] p-[10px] w-[330px]  backdrop-blur-[10px] bg-[#fafafa84] absolute rounded-t-[10px]">
                  <p className="text-[1.5rem] w-full text-center">Fleet Prediction Dashboard</p>
                </div>
{/* 
                <div name="aesthetic-prop" className="w-[8px] aspect-square bg-[#fafafa84] absolute left-[530px] top-[57px]">
                  <div className="w-full h-full rounded-bl-lg bg-[#d9bde3]"></div>
                </div> */}
                <div name="content-container" className="p-[10px] mt-[50px] bg-[#fafafa84] rounded-tl-[0px] rounded-lg">
                
                <section name="Summary" className="items-center justify-between flex relative w-full h-[150px] ">
                   
                   <div className="h-full relative flex-1 flex ml-0 mx-[15px] shadow-sm bg-[#ffffff] rounded-lg overflow-hidden">
                      <section className="flex-col justify-center flex h-full w-[70%] p-[15px] ">
                         <span className="text-[1.3rem] leading-none font-medium">Max Fleet</span>
                         <span className="text-[0.9rem] text-[#626262]">Today</span>
                         <p className="mt-[2px] w-full text-[1.7rem] font-bold bg-gradient-to-r from-[#5EA6EE] to-[#635380] bg-clip-text text-transparent ">
                          50
                            {/* {prediction ? prediction.fleet_required : "-"} */}
                          </p>
                         <p className="mt-[2px] w-full text-[0.8rem] text-green-500 font-medium">+18% increase</p>
                      </section>
                      <div className="right-0 absolute w-[45%] h-full bg-[url('./scooter.png')] bg-cover bg-no-repeat"></div>
                      <section className="h-full  bg-[linear-gradient(200deg,#5EA6EE,#635380)] w-[30%] "> </section>
                   </div>
    
                   <div className="h-full relative flex-1 flex ml-0 mx-[15px] shadow-sm bg-[#ffffff] rounded-lg overflow-hidden">
                      <section className="flex-col justify-center flex h-full w-[70%] p-[15px] ">
                         <span className="text-[1.3rem] leading-none font-medium">Peak Hours</span>
                         <span className="text-[0.9rem] text-[#626262]">Today</span>
                         <p className="mt-[2px] w-full text-[1.7rem] font-bold  bg-[linear-gradient(200deg,#538E38,#d7db5c)] bg-clip-text text-transparent ">8pm - 9pm</p>
                         <p className="mt-[2px] w-full text-[0.8rem] text-green-500 font-medium">+18% increase</p>
                      </section>
                      <div className="right-0 absolute w-[45%] h-full bg-[url('./clock.png')] bg-cover bg-no-repeat"></div>
                      <section className="h-full  bg-[linear-gradient(200deg,#faff70,#538E38)] w-[30%] "> </section>
                   </div>
               
                   <div className="h-full relative flex-1 flex mx-2shadow-sm bg-[#ffffff] rounded-lg overflow-hidden">
                      <section className="flex-col justify-center flex h-full w-[70%] p-[15px] ">
                         <span className="text-[1.3rem] leading-none font-medium">Peak order/hr</span>
                         <span className="text-[0.9rem] text-[#626262]">Today</span>
                         <p className="mt-[2px] w-full text-[1.7rem] font-bold bg-[linear-gradient(200deg,#E67AB2,#75529C)] bg-clip-text text-transparent ">100</p>
                         <p className="mt-[2px] w-full text-[0.8rem] text-green-500 font-medium">+18% increase</p>
                      </section>
                      <div className="right-0 absolute w-[45%] h-full bg-[url('./order.png')] bg-cover bg-no-repeat"></div>
                      <section className="h-full  bg-[linear-gradient(200deg,#E67AB2,#75529C)] w-[30%] "> </section>
                   </div>
                  
                </section>

                <section name="inputGraph-utisation-body" className="flex mt-[15px] w-full gap-[20px]">
                   <div name="input-graph" className="flex justify-center items-center rounded-lg aspect-[3/2] w-1/2 shadow-sm bg-[#ffffff] overflow-hidden">
                        {/* expects js object
                        const chartData = [
                          { hour: 9,  fleet_required: 18 },
                          { hour: 10, fleet_required: 22 },
                          { hour: 11, fleet_required: 26 },
                          { hour: 12, fleet_required: 30 },
                          { hour: 13, fleet_required: 28 },
                          { hour: 14, fleet_required: 25 },
                          { hour: 15, fleet_required: 24 }
                        ]; 
                        Recharts normally shows:
                        9   10   11   12
                        
                        But you want hour ranges, not raw numbers.
                        So when Recharts is about to render an X-axis label:
                        It passes the tick value → h
                        You return a string      
                        */}
                         <BarChart width={600} height={300} data={chartData}>
                          <CartesianGrid strokeDasharray="3 3" />
                          <XAxis
                            dataKey="hour"
                            tickFormatter={(h) => `${h}-${h+1}`}
                          />
                          {/* This tells Recharts:“For each object in chartData, use the value under the key hour for the X-axis.” */}
                          <YAxis />
                          <Tooltip />
                          <Bar dataKey="fleet_required" fill="#5EA6EE" />
                        </BarChart>
                   </div>
                   
                   <div name="utilisation" className="relative aspect-[3/2] w-1/2 shadow-sm bg-[#ffffff] rounded-lg bg-[url('./scooterOutline.png')] bg-contain bg-no-repeat">
                      <div className="absolute z-[10] backdrop-blur-[10px] border-[1.5px] border-[#dfdfdf] bg-[#ebebeb53] p-[10px] bottom-[10px] top-[10px] left-[10px] rounded-lg overflow-hidden">
                         <section className="w-full">Fleet Utilisation Rate:</section>
                         <div className="w-full">
                         </div>
                      </div>
                   </div>
                </section>

                </div>
    
    
                 {/* <div name="gradient" className="absolute bottom-0 h-[70%] w-full bg-[linear-gradient(200deg,#edf6ff_25%,#9FE2FF,#635380)]">
                      
                   </div> */}
            </article>
        </div>
    
   )
};

export default Home;