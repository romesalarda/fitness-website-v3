
import * as React from 'react';
import ListItemButton from '@mui/material/ListItemButton';
import ListItemIcon from '@mui/material/ListItemIcon';
import ListItemText from '@mui/material/ListItemText';
import CreateIcon from '@mui/icons-material/Create';
import PeopleIcon from '@mui/icons-material/People';
import CalendarTodayIcon from '@mui/icons-material/CalendarToday';
// import AssignmentIcon from '@mui/icons-material/Assignment';




export default function MainListItems({ navigate }) {
    return (
        <React.Fragment>
            <ListItemButton onClick={() => navigate("/my-workouts/create-workout/")}>
                <ListItemIcon>
                    <CreateIcon />
                </ListItemIcon>
                <ListItemText primary="Create" />
            </ListItemButton>
            <ListItemButton>
                <ListItemIcon>
                    <CalendarTodayIcon />
                </ListItemIcon>
                <ListItemText primary="Calendar" />
            </ListItemButton>
            <ListItemButton>
                <ListItemIcon>
                    <PeopleIcon />
                </ListItemIcon>
                <ListItemText primary="Sessions" />
            </ListItemButton>

        </React.Fragment>
    )
}

