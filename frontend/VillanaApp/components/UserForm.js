import React, { useState, useEffect } from 'react';
import { View, Text, TextInput, Button, StyleSheet, Image, Alert, TouchableOpacity, FlatList } from 'react-native';
import * as ImagePicker from 'expo-image-picker';

const UserForm = () => {
    const [username, setUsername] = useState('');
    const [email, setEmail] = useState('');
    const [phoneNumber, setPhoneNumber] = useState('');
    const [country, setCountry] = useState('');
    const [password, setPassword] = useState('');
    const [photo, setPhoto] = useState(null);
    const [countries, setCountries] = useState([]);
    const [showCountryList, setShowCountryList] = useState(false);

    useEffect(() => {
        const fetchCountries = async () => {
            try {
                const response = await fetch('http://<votre_domaine>/api/pays/'); // Remplacez par l'URL de votre API
                const data = await response.json();
                setCountries(data);
            } catch (error) {
                console.error('Erreur lors de la récupération des pays:', error);
            }
        };

        fetchCountries();
    }, []);

    const handleImagePicker = async () => {
        let result = await ImagePicker.launchImageLibraryAsync({
            mediaTypes: ImagePicker.MediaTypeOptions.Images,
            allowsEditing: true,
            aspect: [4, 3],
            quality: 1,
        });

        if (!result.canceled) {
            setPhoto(result.assets[0].uri);
        }
    };

    const handleSubmit = async () => {
        if (!phoneNumber) {
            Alert.alert('Erreur', 'Le numéro de téléphone est obligatoire.');
            return;
        }

        const formData = new FormData();
        formData.append('username', username);
        if (email) {
            formData.append('email', email);
        }
        formData.append('phone_number', phoneNumber);
        formData.append('country', country);
        formData.append('password', password);

        if (photo) {
            formData.append('photos', {
                uri: photo,
                type: 'image/jpeg',
                name: 'photo.jpg',
            });
        }

        try {
            const response = await fetch('http://<votre_domaine>/inscription/', {
                method: 'POST',
                body: formData,
            });

            const data = await response.json();
            if (response.ok) {
                console.log(data.message);
                // Envoyer le code d'authentification ici
            } else {
                console.error(data.errors);
            }
        } catch (error) {
            console.error('Erreur lors de l\'inscription:', error);
        }
    };

    return (
        <View style={styles.container}>
            <TouchableOpacity onPress={handleImagePicker}>
                <View style={styles.photoContainer}>
                    {photo ? (
                        <Image source={{ uri: photo }} style={styles.photo} />
                    ) : (
                        <Text style={styles.photoPlaceholder}>Ajouter une photo</Text>
                    )}
                </View>
            </TouchableOpacity>

            <Text style={styles.title}>Inscription</Text>
            <View style={styles.formContainer}>
                <TextInput
                    style={styles.input}
                    placeholder="Nom d'utilisateur"
                    value={username}
                    onChangeText={setUsername}
                />
                <View style={styles.row}>
                    <TextInput
                        style={[styles.input, styles.halfInput]}
                        placeholder="Email (facultatif)"
                        value={email}
                        onChangeText={setEmail}
                        keyboardType="email-address"
                    />
                    <TextInput
                        style={[styles.input, styles.halfInput]}
                        placeholder="Numéro de téléphone (obligatoire)"
                        value={phoneNumber}
                        onChangeText={setPhoneNumber}
                        keyboardType="phone-pad"
                    />
                </View>
                <View style={styles.row}>
                    <TouchableOpacity onPress={() => setShowCountryList(!showCountryList)}>
                        <TextInput
                            style={[styles.input, styles.halfInput]}
                            placeholder="Pays"
                            value={country}
                            editable={false}
                        />
                    </TouchableOpacity>
                </View>
                                {showCountryList && (
                    <FlatList
                        data={countries}
                        keyExtractor={(item) => item.code}
                        renderItem={({ item }) => (
                            <TouchableOpacity onPress={() => {
                                setCountry(item.nom);
                                setShowCountryList(false);
                            }}>
                                <Text style={styles.countryItem}>{item.nom}</Text>
                            </TouchableOpacity>
                        )}
                        style={styles.countryList}
                    />
                )}
                <TextInput
                    style={styles.input}
                    placeholder="Mot de passe"
                    value={password}
                    onChangeText={setPassword}
                    secureTextEntry
                />
                <View style={styles.buttonContainer}>
                    <Button title="S'inscrire" onPress={handleSubmit} color="#fff" />
                </View>
            </View>
        </View>
    );
};

const styles = StyleSheet.create({
    container: {
        flex: 1,
        padding: 20,
        justifyContent: 'center',
    },
    photoContainer: {
        alignItems: 'center',
        justifyContent: 'center',
        width: 120, // Augmenté pour une image plus grande
        height: 120, // Augmenté pour une image plus grande
        borderRadius: 60, // Cercle
        backgroundColor: '#e0e0e0',
        marginBottom: 20,
        overflow: 'hidden',
    },
    photo: {
        width: '100%',
        height: '100%',
        borderRadius: 60,
    },
    photoPlaceholder: {
        color: '#888',
        textAlign: 'center',
    },
    formContainer: {
        backgroundColor: '#f0f0f0',
        borderRadius: 10,
        padding: 20,
        elevation: 3,
    },
    title: {
        fontSize: 24,
        marginBottom: 20,
        textAlign: 'left', // Aligné à gauche
    },
    input: {
        height: 40,
        borderColor: 'gray',
        borderWidth: 1,
        marginBottom: 15,
        paddingHorizontal: 10,
        borderRadius: 5,
    },
    row: {
        flexDirection: 'row',
        justifyContent: 'space-between',
        marginBottom: 15,
    },
    halfInput: {
        flex: 1,
        marginRight: 5,
    },
    countryList: {
        maxHeight: 150,
        backgroundColor: '#fff',
        borderRadius: 5,
        elevation: 2,
        marginBottom: 15,
    },
    countryItem: {
        padding: 10,
        borderBottomWidth: 1,
        borderBottomColor: '#ccc',
    },
    buttonContainer: {
        alignItems: 'flex-end', // Aligner le bouton à droite
    },
});

export default UserForm;