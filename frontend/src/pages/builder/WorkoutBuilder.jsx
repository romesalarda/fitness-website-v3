import React, { useEffect, useState } from 'react'
import { useParams, useSearchParams } from 'react-router-dom';
// mui
import Box from '@mui/material/Box';
import Paper from '@mui/material/Paper';
import Grid from '@mui/material/Grid';
import Pagination from '@mui/material/Pagination';
import SaveAltIcon from '@mui/icons-material/SaveAlt';
import Fab from '@mui/material/Fab';
// components
import ExerciseInput from './ExerciseInput';
import WorkoutExercises from './UserExercises';
// components
// import WorkoutSearchBar from '../page/WorkoutSearchBar';
// import SetListItem from './SetListItem';
// import AddSetListItem from './AddSetListItem';
// import EmptyPage from '../extra/EmptyPage';
// import CreateSetInput from './SetInput';
// import AlertComponent from '../extra/AlertComponent';
// import SimpleAlertComponent from '../extra/SimpleAlertComponent';
// import MultipleSelect from '../extra/MultiSelect';

// view page to edit a user workout
function WorkoutBuilder(any) {
    const params = useParams()
    // // workout app state
    // const [workoutData, setWorkoutData] = useState({
    //     sets: [],
    //     name: '',
    //     id: null,
    // });
    // const [successMessage, setSuccessMessage] = useState(null)
    // // input error messages
    // const [creationError, setCreationError] = useState(null)

    // const [appendError, setAppendError] = useState(null)
    // const [alertMessage, setAlertMessage] = useState(null)
    // // pagination
    // const [pagination, setPagination] = useState({
    //     page: 1, // starting page
    //     show: 2, // determines how many workouts to show per page
    // })
    // const [newSetInpt, setNewSetInpt] = useState("")
    // const [searchedSets, setSearchedSets] = useState([])

    // const handlePageChange = (event, value) => {
    //     setPagination({ ...pagination, page: value });
    // };

    // const handleDismissAlert = () => {
    //     setAlertMessage(null)
    // }

    // // CRUD 
    // const handleCreateSet = (e) => {
    //     setCreationError(null)
    //     e.preventDefault()
    //     axiosInstance.post("/workout/" + workoutData.id + "/create-add-set/", {
    //         title: e.target[0].value,
    //         repetitions: e.target[1].value,
    //         sets: e.target[2].value,
    //         public: e.target[3].checked
    //     }).then((res) => {
    //         setWorkoutData({ ...workoutData, sets: [res.data, ...workoutData.sets] })
    //         setNewSetInpt("")
    //     }).catch(err => {
    //         setCreationError(err.response.data.detail)
    //     })
    // }
    // const handleWorkoutSave = () => {
    //     axiosInstance.put("/workout/" + workoutData.id + "/update/", {
    //         sets: workoutData.sets
    //     }).then(res => {

    //         setSuccessMessage("Successfully saved workout!")
    //     })
    // }
    // const handleRemoveSet = (id) => {
    //     console.log("hello")
    //     axiosInstance.delete("/set-remove/", {
    //         data: {
    //             set_id: id,
    //             workout_id: workoutData.id
    //         }
    //     }).then((res) => {
    //         setWorkoutData({ ...workoutData, sets: workoutData.sets.filter(e => e.id !== id) })
    //     })
    // }
    // const handleDeleteSet = (id) => {
    //     axiosInstance.delete("/set-delete/", {
    //         data: {
    //             set_id: id,
    //             workout_id: workoutData.id
    //         }
    //     }).then((res) => {
    //         setWorkoutData({ ...workoutData, sets: workoutData.sets.filter(e => e.id !== id) })
    //         setSearchedSets(searchedSets.filter(s => s.id !== id))
    //         setSuccessMessage("successfully deleted set")
    //     })
    // }
    // // handles the number of pages which should be shown
    // const handleGetPages = () => {
    //     if (workoutData.sets.length >= pagination.show) {
    //         return Math.round(workoutData.sets.length / pagination.show)
    //     }
    //     return 1
    // };
    // // handle searching for workout
    // const handleWorkoutSearch = (e) => {
    //     setAppendError(null)
    //     e.preventDefault()
    //     const categories = e.target[2].value
    //     const search = e.target[0].value
    //     axiosInstance.get("/sets/", { params: { search: search, public: true, categories: categories } }).then((res) => {
    //         const sets = res.data;
    //         setSearchedSets(sets)
    //     });
    // }
    // const handleAddSet = (set, copy) => {
    //     axiosInstance.put("/workout/" + workoutData.id + "/add-set/", {
    //         set_id: set.id,
    //         copy
    //     }).then(res => {
    //         setWorkoutData({ ...workoutData, sets: [res.data, ...workoutData.sets] })
    //         setSuccessMessage(`Successfully added '${set.title}'`)
    //     }).catch(err => {
    //         setSuccessMessage(null)
    //         setAlertMessage(err.response.data.detail)
    //     })
    // }

    useEffect(() => {
        // fetch workout data
        // axiosInstance.get("/workout/" + params.slug).then((res) => {
        //     const workout = res.data;
        //     setWorkoutData({ sets: workout.sets, name: workout.title, id: workout.id })
        // });
        // console.log(params.uuid)

    })

    return (
        <React.Fragment>

            <Box sx={{ flexGrow: 4, margin: 4 }}>
                <Grid container spacing={12} justifyContent="center" sx={{ maxHeight: "80vh" }}>
                    <Grid item xs>
                        {/* search function to add new workouts */}
                        <Paper elevation={3} sx={{ bgcolor: "lightgrey", minHeight: "50vh", padding: 1 }}>

                        </Paper>
                    </Grid>
                    <Grid item md>
                        {/* area to see current workouts */}
                        <Paper elevation={3} sx={{ bgcolor: "lightgrey", minHeight: "50vh", padding: 1 }}>
                            <ExerciseInput />
                            <WorkoutExercises workoutID={params.uuid} />
                        </Paper>
                    </Grid>

                </Grid>

                <Fab color="success" aria-label="add" sx={{
                    position: "fixed", right: "5vh", bottom: "5vh", width: "10vh", height: "10vh"
                }} size="large" onClick={() => console.log("save workout")}>
                    Save <SaveAltIcon />
                </Fab>
            </Box>
        </React.Fragment>

    )
}

export default WorkoutBuilder