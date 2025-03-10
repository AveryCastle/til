class SyncService {
  final Database _db;
  final ConnectivityResult _connectivity;

  Future<void> syncData() async {
    if (await _hasInternetConnection()) {
      final localChanges = await _getLocalChanges();
      await _uploadChanges(localChanges);
      await _downloadNewData();
    }
  }

  Future<void> saveOfflineData(Flashcard card) async {
    await _db.insert('offline_changes', {
      'english': card.english,
      'korean': card.korean,
      'dayNumber': card.dayNumber,
      'timestamp': DateTime.now().toIso8601String(),
    });
  }
} 