import React, { useEffect, useState, useRef } from 'react';
import { View, Text, Image, StyleSheet, TouchableOpacity, ScrollView, Modal, BackHandler, Animated } from 'react-native';
import { useNavigation, useRoute } from '@react-navigation/native';

const Item = () => {
  const navigation = useNavigation();
  const route = useRoute();
  const { image, titre, artiste, prix, fichier_audio } = route.params; // Récupérer les paramètres
  const [modalVisible, setModalVisible] = useState(true);
  const fadeAnim = useRef(new Animated.Value(0)).current;

  useEffect(() => {
    // Animation d'apparition
    Animated.timing(fadeAnim, {
      toValue: 1,
      duration: 100,
      useNativeDriver: true,
    }).start();

    // Gestionnaire d'événement pour le bouton de retour
    const backHandler = BackHandler.addEventListener('hardwareBackPress', _handleBackPress);
    return () => {
      // Nettoyer l'événement
      backHandler.remove();
    };
  }, []);

  const _handleBackPress = () => {
    _closeModal();
    return true;
  };

  const _closeModal = () => {
    // Animation de disparition
    Animated.timing(fadeAnim, {
      toValue: 0,
      duration: 200,
      useNativeDriver: true,
    }).start(() => {
      setModalVisible(false);
      navigation.goBack();
    });
  };

  return (
    <Modal
      animationType="fade"
      transparent={true}
      visible={modalVisible}
      onRequestClose={_closeModal}
    >
      <TouchableOpacity
        style={styles.modalOverlay}
        activeOpacity={1}
        onPress={_closeModal}
      >
        <Animated.View
          style={[styles.modalContainer, { opacity: fadeAnim }]}
        >
          <View style={styles.modalContent}>
            <ScrollView contentContainerStyle={styles.container}>
              <View style={styles.albumImageContainer}>
                <Image
                  source={{ uri: image }}
                  style={styles.albumim}
                />
              </View>

              <Text style={styles.albumTitle}>{titre}</Text>
              <Text style={styles.albumPrice}>{prix} XOF</Text>
              <Text style={styles.salesInfo}>0 Vente</Text>

              <TouchableOpacity style={styles.vipButton}>
                <Text style={styles.vipButtonText}>Achats VIP</Text>
              </TouchableOpacity>
              <Text style={styles.vipInfo}>
                Faire un achat VIP de soutien.
              </Text>

              <Text style={styles.albumDescription}>
                {artiste} vous propose un album intitulé "{titre}".
              </Text>

              <TouchableOpacity style={styles.buyButton}>
                <Text style={styles.buyButtonText}>Acheter maintenant</Text>
              </TouchableOpacity>
            </ScrollView>
          </View>
        </Animated.View>
      </TouchableOpacity>
    </Modal>
  );
};

// Styles...

const styles = StyleSheet.create({
  container: {
    flexGrow: 1,
    backgroundColor: '#fff',
    alignItems: 'center',
  },
  modalOverlay: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: 'rgba(0, 0, 0, 0.5)',
  },
  modalContainer: {
    width: '90%',
    height: '80%',
    backgroundColor: '#fff',
    borderRadius: 10,
    overflow: 'hidden',
  },
  modalContent: {
    flex: 1,
    backgroundColor: '#fff',
    borderRadius: 10,
  },
  albumImageContainer: {
    backgroundColor: '#444',
    width: '100%',
    height: 350,
    justifyContent: 'center',
    alignItems: 'center',
  },
  albumTitle: {
    color: '#052c65',
    fontSize: 18,
    fontWeight: 'bold',
    textAlign: 'center',
    marginVertical: 10,
  },
  albumPrice: {
    color: '#052c65',
    fontSize: 20,
    fontWeight: 'bold',
    textAlign: 'center',
    marginTop: 10,
  },
  albumim: {
    width: 350,
    height: 250,
    borderRadius: 10,
    backgroundColor: '#fff',
  },
  salesInfo: {
    color: '#fff',
    fontSize: 14,
    textAlign: 'center',
    marginTop: 5,
  },
  vipButton: {
    borderColor: '#00AA00',
    borderWidth: 1,
    borderRadius: 5,
    paddingVertical: 5,
    paddingHorizontal: 10,
    marginTop: 10,
  },
  vipButtonText: {
    color: '#00AA00',
    fontSize: 14,
    textAlign: 'center',
  },
  albumDescription: {
    color: '#444',
    fontSize: 16,
    textAlign: 'center',
    marginVertical: 10,
  },
  buyButton: {
    backgroundColor: '#f41',
    borderRadius: 25,
    paddingVertical: 10,
    paddingHorizontal: 20,
    marginTop: 10,
  },
  buyButtonText: {
    color: '#fff',
    fontSize: 16,
    textAlign: 'center',
  },
  vipInfo: {
    color: '#a1e401',
    fontSize: 14,
    textAlign: 'center',
    marginVertical: 10,
  },
});

export default Item;
