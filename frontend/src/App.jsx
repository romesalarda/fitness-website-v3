
import './App.css';


import { useMutation, useQuery, useQueryClient } from 'react-query'
import axiosInstance from './axios';



function App() {
  const queryClient = useQueryClient();

  const { isLoading, error, data } = useQuery("workouts", () =>
    axiosInstance.get("/workouts/").then((res) => {
      return res.data
    }))

  const addWorkout = useMutation(newWorkout => {
    return axiosInstance.post("/workouts/", newWorkout)
  }, {
    onSuccess: () => {
      queryClient.invalidateQueries("workouts")
    }
  }
  )

  if (isLoading) return 'Loading...'

  if (error) return 'An error has occurred: ' + error.message



  return (
    <div className="App">
      <p>data is :{JSON.stringify(data)}</p>
      <p>hello?</p>
      <button onClick={() => addWorkout.mutate({ title: "please work" })}>press me</button>
    </div>
  );
}

export default App;
