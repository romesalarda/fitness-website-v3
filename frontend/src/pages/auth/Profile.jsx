import React, { useEffect, useState } from 'react'
import axiosInstance from '../../axios';


function Profile() {
    const [profileDetails, setprofileDetails] = useState(null)

    useEffect(() => {
        // fetch profile details
        axiosInstance.get("/user/profile").then((res) => {
            const data = res.data;
            setprofileDetails(data)
        });
    }, []);
    return (
        <div>{JSON.stringify(profileDetails)}</div>
    )
}

export default Profile