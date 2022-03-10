import React, { useEffect, useState } from 'react'
// mui
import Card from '@mui/material/Card';
import DeleteIcon from '@mui/icons-material/Delete';

import CardContent from '@mui/material/CardContent';
import CardActions from '@mui/material/CardActions';
import Grid from '@mui/material/Grid';
import Stack from '@mui/material/Stack';
import TextField from '@mui/material/TextField';
import Checkbox from '@mui/material/Checkbox';
import PublicIcon from '@mui/icons-material/Public';
import PublicOffIcon from '@mui/icons-material/PublicOff';
import { MenuItem, Select, InputLabel, FormControl, IconButton, Divider } from '@mui/material';
import SwapHorizIcon from '@mui/icons-material/SwapHoriz';

import EditIcon from '@mui/icons-material/Edit';

export default function CardioEdit({ data, handleSwitch }) {
    const [exerciseData, setExerciseData] = useState(data)
    // const [errorMessage, setErrorMessage] = useState(null)

    const updateExercise = (e) => {
        setExerciseData({
            ...exerciseData,
            [e.target.id]: e.target.value.trim(),
        });
    };


    return (
        <Card sx={{ minWidth: 275, bgcolor: "lightgrey", margin: 2 }} variant="outlined">
            <CardContent>
                <Grid container>
                    <TextField
                        id="title"
                        value={data.title}
                        variant="standard"
                        type="text"
                        size="small"
                        fullWidth
                        sx={{ margin: 1 }}
                    />
                    <Grid item xs={3} md={6}>
                        <Card sx={{ margin: 1 }}>
                            <Stack>
                                <Stack spacing={2} sx={{ padding: 1 }} direction="row">
                                    <TextField
                                        id="repetitions"
                                        label="Repetitions"
                                        variant="outlined"
                                        type="text"
                                        size="large"
                                        onChange={updateExercise}
                                        sx={{ flex: 6 }}
                                    />
                                    <FormControl>
                                        <InputLabel id="repetiton-unit-lable">Unit</InputLabel>
                                        <Select
                                            labelId="repetiton-unit-lable"
                                            id="repetiton-unit-select"
                                            value={1}
                                            label="Unit"
                                            onChange={updateExercise}
                                            sx={{ flex: 2 }}
                                        >
                                            <MenuItem value={1}>Seconds</MenuItem>
                                            <MenuItem value={2}>Minutes</MenuItem>
                                            <MenuItem value={3}>Until Failure</MenuItem>
                                        </Select>
                                    </FormControl>
                                </Stack>
                                <TextField
                                    id="sets"
                                    label="Sets"
                                    variant="outlined"
                                    type="text"
                                    size="large"
                                    onChange={updateExercise}
                                    sx={{ margin: 1 }}
                                />
                            </Stack>

                        </Card>

                    </Grid>
                    <Grid item xs={3} md={6}>
                        <Card sx={{ margin: 1 }}>
                            <Stack spacing={2} sx={{ padding: 1 }} direction="row">
                                <TextField
                                    id="weight"
                                    label="Weight"
                                    variant="outlined"
                                    type="number"
                                    size="large"
                                    onChange={updateExercise}
                                    sx={{ flex: 6 }}
                                />
                                <FormControl >
                                    <InputLabel id="weight-unit-lable">Unit</InputLabel>
                                    <Select
                                        labelId="weight-unit-lable"
                                        id="weight-unit-select"
                                        value={1}
                                        label="Unit"
                                        onChange={updateExercise}
                                        sx={{ flex: 2 }}
                                    >
                                        <MenuItem value={1}>Meters</MenuItem>
                                        <MenuItem value={2}>Kilometers</MenuItem>
                                    </Select>
                                </FormControl>

                            </Stack>
                        </Card>

                    </Grid>
                </Grid>
            </CardContent>
            <Divider></Divider>
            <CardActions disableSpacing sx={{ justifyContent: "right" }}>

                <IconButton>
                    <EditIcon />
                </IconButton>
                <IconButton>
                    <DeleteIcon />
                </IconButton>
                <Checkbox
                    id="public"

                    checked={true}
                    icon={<PublicOffIcon />}
                    checkedIcon={<PublicIcon />}
                />
                <IconButton onClick={() => handleSwitch(true)}>
                    <SwapHorizIcon />
                </IconButton>


            </CardActions>
        </Card>
    )
}