// mui
import Button from '@mui/material/Button';
import Stack from '@mui/material/Stack';
import Typography from '@mui/material/Typography';
import ListItem from '@mui/material/ListItem';
import ButtonGroup from '@mui/material/ButtonGroup';
import ListItemAvatar from '@mui/material/ListItemAvatar';
import Avatar from '@mui/material/Avatar';
// icons
import FitnessCenterIcon from '@mui/icons-material/FitnessCenter';
import DeleteIcon from '@mui/icons-material/Delete';
import EditIcon from '@mui/icons-material/Edit';
// react
import { useNavigate } from 'react-router-dom'
import React from 'react';

export default function WorkoutItem({ details, handleDelete }) {
    const navigate = useNavigate()
    // individual workout item 
    return (
        <ListItem secondaryAction={
            <ButtonGroup>
                <Button variant="contained" color="error" onClick={() => handleDelete(details)}>
                    <DeleteIcon />
                </Button>
                <Button variant="contained" onClick={() => navigate("/my-workouts/" + details.id + "/edit")}>
                    <EditIcon />
                </Button>
                <Button variant="contained" color="success">
                    <FitnessCenterIcon />
                </Button>
            </ButtonGroup>
        } sx={{ margin: 2 }}
            disablePadding>
            <ListItemAvatar>
                <Avatar>
                    <FitnessCenterIcon />
                </Avatar>
            </ListItemAvatar>
            <Stack>
                <Typography variant="h5">
                    {details.title}
                </Typography>
                <Typography>
                    Created: {new Date(details.created).toUTCString()}
                </Typography>

            </Stack>
        </ListItem>
    );
}


