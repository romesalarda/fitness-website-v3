import React from 'react'

import Paper from '@mui/material/Paper';
import IconButton from '@mui/material/IconButton';
import AddIcon from '@mui/icons-material/Add';
import Switch from '@mui/material/Switch';
import FormControlLabel from '@mui/material/FormControlLabel';
import FormGroup from '@mui/material/FormGroup';

import TextField from '@mui/material/TextField';


// create new set
export default function ExerciseInput({ handleCreate, handleChangeInput, value }) {
    return (
        <Paper
            component="form"
            sx={{ p: '10px 4px', display: 'flex', alignItems: 'center', margin: 2 }}
            onSubmit={handleCreate}
        >
            <TextField
                sx={{ ml: 1, flex: 3 }}
                placeholder="Create new exercise"
                inputProps={{ 'aria-label': 'create new set' }}
                fullWidth
                size='small'
                required
                value={value}
                onChange={handleChangeInput}
                variant="standard"
            />
            <TextField
                sx={{ ml: 1, flex: 1 }}
                placeholder="Repetitions"
                type="number"
                inputProps={{ 'aria-label': 'repetitions' }}
                fullWidth
                size='small'
                required
                defaultValue={12}
                variant="standard"
                InputProps={{ inputProps: { min: 1 } }}
                label="repetitions"
            />
            <TextField
                sx={{ ml: 1, flex: 1 }}
                placeholder="Sets"
                inputProps={{ 'aria-label': 'sets' }}
                fullWidth
                size='small'
                required
                type="number"
                InputProps={{ inputProps: { min: 0 } }}
                defaultValue={4}
                variant="standard"
                label="sets"
            />
            <FormGroup sx={{ ml: 1, flex: 1 }}>
                <FormControlLabel control={<Switch label="public" />} label="Global" />
            </FormGroup>
            <IconButton type="submit" sx={{ p: '10px' }} aria-label="search">
                <AddIcon />
            </IconButton>

        </Paper>
    )
}
