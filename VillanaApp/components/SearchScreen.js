import React, { useState } from 'react';
import { View, Text, StyleSheet, TextInput, TouchableOpacity, FlatList, Modal } from 'react-native';
import AppBar from './AppBar';

const SearchScreen = () => {
  const [username, setUsername] = useState('');
  const [advancedSearchVisible, setAdvancedSearchVisible] = useState(false);
  const [price, setPrice] = useState('');
  const [neighborhood, setNeighborhood] = useState('');
  const [surface, setSurface] = useState('');
  const [houseType, setHouseType] = useState('');
  const [results, setResults] = useState([]);
  const [modalVisible, setModalVisible] = useState(true); // État pour contrôler la visibilité du modal principal

  const handleSearch = () => {
    // Logique de recherche pour les noms d'utilisateur
    const filteredResults = []; // Remplacez par vos résultats filtrés
    setResults(filteredResults);
  };

  const handleAdvancedSearch = () => {
    // Logique de recherche avancée
    const advancedResults = []; // Remplacez par vos résultats filtrés
    setResults(advancedResults);
    setAdvancedSearchVisible(false);
  };

  return (
    <View style={styles.container}>
    <Modal
      visible={modalVisible}
      animationType="slide"
      transparent={false} // Assurez-vous que le modal prend tout l'écran
      onRequestClose={() => setModalVisible(false)} // Ferme le modal
    >
      <AppBar/> 
      
        <View style={styles.Headerinput}>
          <TextInput
            style={styles.input}
            placeholder="Rechercher un nom d'utilisateur"
            placeholderTextColor={'#444'}
            value={username}
            onChangeText={setUsername}
          />
          <TouchableOpacity style={styles.button} onPress={handleSearch}>
            <Text style={styles.buttonText}>Rechercher</Text>
          </TouchableOpacity>
        </View>

        <View >
          <TouchableOpacity style={styles.advancedButton} onPress={() => setAdvancedSearchVisible(true)}>
            <Text style={styles.buttonText}>Recherche une Maison</Text>
          </TouchableOpacity>
        </View>

        <FlatList
          data={results}
          keyExtractor={(item, index) => index.toString()}
          renderItem={({ item }) => <Text style={styles.resultItem}>{item}</Text>}
        />

        <Modal
          visible={advancedSearchVisible}
          animationType='fade'
          transparent={true}
          onRequestClose={() => setAdvancedSearchVisible(false)}
        >
          <View style={styles.modalContainer}>
            <View style={styles.modalRow}>
              <TextInput
                style={styles.inputmodal}
                placeholder="Prix"
                placeholderTextColor="#000"
                value={price}
                onChangeText={setPrice}
              />
              <TextInput
                style={styles.inputmodal}
                placeholder="Quartier"
                placeholderTextColor="#000"
                value={neighborhood}
                onChangeText={setNeighborhood}
              />
            </View>
            <View style={styles.modalRow}>
              <TextInput
                style={styles.inputmodal}
                placeholder="Surface"
                placeholderTextColor="#000"
                value={surface}
                onChangeText={setSurface}
              />
              <TextInput
                style={styles.inputmodal}
                placeholder="Type de maison (étage/villa)"
                placeholderTextColor="#000"
                value={houseType}
                onChangeText={setHouseType}
              />
            </View>
            <View style={styles.buttonbas}>
              <TouchableOpacity style={styles.button2} onPress={handleAdvancedSearch}>
                <Text style={styles.buttonText}>Rechercher</Text>
              </TouchableOpacity>
              <TouchableOpacity style={styles.closeButton} onPress={() => setAdvancedSearchVisible(false)}>
                <Text style={styles.buttonText}>Fermer</Text>
              </TouchableOpacity>
            </View>
          </View>
        </Modal>
      
    </Modal>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    marginTop:100
  },
  Headerinput: {
    
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'flex-start',
    marginHorizontal: 20,
    marginTop: 100,
  },
  input: {
    height: 40,
    width: 250, // Ajustez la largeur si nécessaire
    borderColor: 'gray',
    borderWidth: 1,
    marginBottom: 10,
    borderRadius: 15,
    paddingHorizontal: 10,
  },
  inputmodal: {
    height: 40,
    width: 180, // Ajustez la largeur si nécessaire
    borderColor: 'gray',
    borderWidth: 1,
    marginBottom: 10,
    borderRadius: 15,
    paddingHorizontal: 10,
  },
  button: {
    backgroundColor: 'grey',
    padding: 10,
    marginLeft: 20,
    borderRadius: 15,
  },
  button2: {
    backgroundColor: 'grey',
    padding: 10,
    borderRadius: 15,
    alignItems: 'center',
    justifyContent: 'center',
  },
  advancedButton: {
    backgroundColor: 'green',
    padding: 10,
    alignItems: 'center',
    justifyContent: 'center',
    borderRadius: 15,
    marginTop: 10,
  },
  buttonText: {
    color: 'white',
  },
  buttonbas: {
    flexDirection: 'row',
    justifyContent: 'space-between',
  },
  resultItem: {
    padding: 10,
    borderBottomWidth: 1,
    borderBottomColor: '#ccc',
  },
  modalContainer: {
    flex: 1,
    padding: 20,
    backgroundColor: 'white',
    justifyContent: 'flex-start', // Aligne les éléments en haut
    marginTop: 200,
  },
  modalRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginBottom: 10,
  },
  closeButton: {
    backgroundColor: 'red',
    padding: 10,
    alignItems: 'center',
    borderRadius: 15,
    marginTop: 10,
  },
});

export default SearchScreen;