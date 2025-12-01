import React, { useEffect, useState } from 'react';
import { View, Text, Image } from 'react-native';
import axios from 'axios';

const MaisonDetail = ({ route }) => {
  const [maison, setMaison] = useState(null);
  const { id } = route.params;  // L'ID de la maison passé par la navigation

  useEffect(() => {
    axios.get(`http://localhost:8000/maisons/${id}/`)  // Mets ton URL d'API ici
      .then(response => {
        setMaison(response.data);
      })
      .catch(error => {
        console.error(error);
      });
  }, [id]);

  if (!maison) {
    return <Text>Chargement...</Text>;
  }

  return (
    <View>
      <Text>{maison.titre}</Text>
      <Text>{maison.description}</Text>
      <Text>{maison.prix} €</Text>
      {maison.photos && (
        <Image source={{ uri: maison.photos }} style={{ width: 200, height: 200 }} />
      )}
    </View>
  );
};

export default MaisonDetail;
