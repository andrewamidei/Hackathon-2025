import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import '../chat/chat_page.dart';

class ContactsPage extends StatelessWidget {
  final String currentUser;

  const ContactsPage({
    super.key,
    required this.currentUser,
  });

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Contacts'),
        actions: [
          IconButton(
            icon: const Icon(Icons.add),
            onPressed: () {
              // Show dialog to add new contact
              _showAddContactDialog(context);
            },
          ),
        ],
      ),
      body: FutureBuilder<List<String>>(
        future: _fetchContacts(currentUser),
        builder: (context, snapshot) {
          if (snapshot.connectionState == ConnectionState.waiting) {
            return const Center(child: CircularProgressIndicator());
          }

          if (snapshot.hasError) {
            return Center(child: Text('Error: ${snapshot.error}'));
          }

          final contacts = snapshot.data ?? [];
          
          return ListView.builder(
            itemCount: contacts.length,
            itemBuilder: (context, index) {
              return ListTile(
                leading: CircleAvatar(
                  child: Text(contacts[index][0].toUpperCase()),
                ),
                title: Text(contacts[index]),
                onTap: () {
                  Navigator.push(
                    context,
                    MaterialPageRoute(
                      builder: (context) => ChatPage(
                        currentUser: currentUser,
                        receiver: contacts[index],
                      ),
                    ),
                  );
                },
              );
            },
          );
        },
      ),
    );
  }

  Future<void> _showAddContactDialog(BuildContext context) async {
    final controller = TextEditingController();
    return showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('Add Contact'),
        content: TextField(
          controller: controller,
          decoration: const InputDecoration(
            labelText: 'Username',
          ),
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context),
            child: const Text('Cancel'),
          ),
          TextButton(
            onPressed: () async {
              // Add contact API call here
              // await addContact(currentUser, controller.text);
              Navigator.pop(context);
            },
            child: const Text('Add'),
          ),
        ],
      ),
    );
  }

  Future<List<String>> _fetchContacts(String username) async {
    // TODO: Implement API call to fetch contacts
    // For now, return dummy data
    await Future.delayed(const Duration(seconds: 1));
    return ['alice', 'bob', 'charlie'];
  }
}