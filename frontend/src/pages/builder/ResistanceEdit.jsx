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

export default function ResistanceEdit({ data, handleSwitch, updateTextFields, updateSelectFields }) {
    // const [errorMessage, setErrorMessage] = useState(null)
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
                        onChange={updateTextFields}
                    />
                    <Grid item xs={3} md={6}>
                        <Card sx={{ margin: 1 }}>
                            <Stack>
                                <Stack spacing={2} sx={{ padding: 1 }} direction="row">
                                    <TextField
                                        id="repetitions"
                                        label="repetitions"
                                        variant="outlined"
                                        type="number"
                                        size="large"
                                        value={data.repetitions}
                                        onChange={updateTextFields}
                                        sx={{ flex: 6 }}
                                    />
                                    <FormControl>
                                        <InputLabel id="repetiton-unit-lable">Unit</InputLabel>
                                        <Select
                                            labelId="repetiton-unit-lable"
                                            id="repetitions_unit"
                                            name="repetitions_unit"
                                            value={data.repetitions_unit}
                                            label="Unit"
                                            onChange={updateSelectFields}
                                            sx={{ flex: 2 }}
                                        >
                                            <MenuItem value={"1"}>Reps</MenuItem>
                                            <MenuItem value={"2"}>Until failure</MenuItem>
                                        </Select>
                                    </FormControl>
                                </Stack>
                                <TextField
                                    id="sets"
                                    label="sets"
                                    variant="outlined"
                                    type="number"
                                    size="large"
                                    onChange={updateTextFields}
                                    sx={{ margin: 1 }}
                                    value={data.sets}
                                />
                            </Stack>

                        </Card>

                    </Grid>
                    <Grid item xs={3} md={6}>
                        <Card sx={{ margin: 1 }}>
                            <Stack spacing={2} sx={{ padding: 1 }} direction="row">
                                <TextField
                                    id="weight"
                                    label="weight"
                                    variant="outlined"
                                    type="number"
                                    size="large"
                                    sx={{ flex: 6 }}
                                    value={data.weight}
                                    onChange={updateTextFields}
                                />
                                <FormControl>
                                    <InputLabel id="weight-unit-lable">Unit</InputLabel>
                                    <Select
                                        labelId="weight-unit-lable"
                                        id="weight_unit"
                                        value={data.weight_unit}
                                        label="unit"
                                        name="weight_unit"
                                        sx={{ flex: 2 }}
                                        onChange={updateSelectFields}
                                    >
                                        <MenuItem value={"1"}>Kg</MenuItem>
                                        <MenuItem value={"2"}>Pb</MenuItem>
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
                <IconButton onClick={() => handleSwitch(false)}>
                    <SwapHorizIcon />
                </IconButton>


            </CardActions>
        </Card>
    )
}