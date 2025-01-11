import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';

function BeachParams() {
  const { stateId, beach } = useParams(); // Dynamic URL parameters
  const [beachDetails, setBeachDetails] = useState(null); // Store dynamic beach details (lat, long)
  const [loading, setLoading] = useState(true); // Loading state
  const [error, setError] = useState(''); // Error state

  // Static data remains unchanged
  const staticData = {
    Goa: {
      Panaji: {
        'Miramar': {
          temperature: 25,
          uvIndex: 7,
          precipitation: 30,
          sunsetTime: '18:00',
          sunriseTime: '06:00',
        },
        'Dona Paula': {
          temperature: 24,
          uvIndex: 6,
          precipitation: 25,
          sunsetTime: '17:45',
          sunriseTime: '06:15',
        },
      },
      Calangute: {
        'Calangute': {
          temperature: 26,
          uvIndex: 8,
          precipitation: 20,
          sunsetTime: '18:15',
          sunriseTime: '06:30',
        },
        'Baga': {
          temperature: 25,
          uvIndex: 7,
          precipitation: 22,
          sunsetTime: '18:00',
          sunriseTime: '06:20',
        },
      },
    },
    Kerala: {
      Kochi: {
        'Fort Kochi': {
          temperature: 28,
          uvIndex: 9,
          precipitation: 35,
          sunsetTime: '18:30',
          sunriseTime: '06:45',
        },
        'Cherai': {
          temperature: 27,
          uvIndex: 8,
          precipitation: 30,
          sunsetTime: '18:20',
          sunriseTime: '06:40',
        },
      },
      Alappuzha: {
        'Alappuzha': {
          temperature: 29,
          uvIndex: 10,
          precipitation: 40,
          sunsetTime: '18:45',
          sunriseTime: '07:00',
        },
        'Marari': {
          temperature: 28,
          uvIndex: 9,
          precipitation: 35,
          sunsetTime: '18:35',
          sunriseTime: '06:55',
        },
      },
    },
    TamilNadu: {
      Chennai: {
        'Marina': {
          temperature: 30,
          uvIndex: 11,
          precipitation: 45,
          sunsetTime: '19:00',
          sunriseTime: '07:10',
        },
        'Elliot\'s': {
          temperature: 29,
          uvIndex: 10,
          precipitation: 40,
          sunsetTime: '18:50',
          sunriseTime: '07:05',
        },
      },
      Mahabalipuram: {
        'Mahabalipuram': {
          temperature: 31,
          uvIndex: 12,
          precipitation: 50,
          sunsetTime: '19:15',
          sunriseTime: '07:20',
        },
      },
    },
  };

  const stateData = staticData[stateId];
  const cityData = stateData ? stateData[Object.keys(stateData)[0]] : null; // Assuming city is not dynamic in the static data

  // Dynamic fetching for latitude and longitude based on stateId and beach
  useEffect(() => {
    const fetchBeachDetails = async () => {
      try {
        setLoading(true);

        // Fetch latitude and longitude from the backend
        const response = await fetch(`http://localhost:7200/location/${stateId}/${beach}`, {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
          },
        });

        const data = await response.json();

        if (!response.ok) {
          throw new Error(data.error || 'Failed to fetch beach details');
        }

        setBeachDetails(data); // Set the latitude and longitude
        setLoading(false);
      } catch (err) {
        setError(err.message);
        setLoading(false);
      }
    };

    if (stateId && beach) {
      fetchBeachDetails();
    }
  }, [stateId, beach]);

  if (loading) {
    return <div>Loading beach details...</div>;
  }

  if (error) {
    return <div>Error: {error}</div>;
  }

  const staticBeachDetails = cityData ? cityData[beach] : null;

  if (!staticBeachDetails) {
    return <div>Sorry, no static data found for the beach: {beach} in {stateId}.</div>;
  }

  return (
    <div className='find-beaches'>
      <h2>{beach} Details in {stateId}</h2>
      <ul>
        {/* Static data rendering */}
        <li>
          <strong>Temperature: </strong>
          <span>{staticBeachDetails.temperature}°C</span>
        </li>
        <li>
          <strong>UV Ray Index: </strong>
          <span>{staticBeachDetails.uvIndex}</span>
        </li>
        <li>
          <strong>Precipitation: </strong>
          <span>{staticBeachDetails.precipitation}%</span>
        </li>
        <li>
          <strong>Sunrise Time: </strong>
          <span>{staticBeachDetails.sunriseTime}</span>
        </li>
        <li>
          <strong>Sunset Time: </strong>
          <span>{staticBeachDetails.sunsetTime}</span>
        </li>

        {/* Dynamic data rendering */}
        <li>
          <strong>Latitude: </strong>
          <span>{beachDetails.latitude}</span>
        </li>
        <li>
          <strong>Longitude: </strong>
          <span>{beachDetails.longitude}</span>
        </li>
      </ul>
    </div>
  );
}

export default BeachParams;
