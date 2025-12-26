from app.services.conversation.conversation_service import ConversationService

service = ConversationService()

# Test normalization
test_cases = [
    ('What do you eat for breakfast?', 'what do you eat for breakfast'),
    ('What do you eat for breakfast', 'what do you eat for breakfast'),
    ('WHAT DO YOU EAT FOR BREAKFAST?!', 'what do you eat for breakfast'),
    ('¿Cómo estás?', 'cómo estás'),
    ('Como estas', 'como estas'),
]

print('Normalization test - works both with or without punctuation:')
print()
for original, expected in test_cases:
    normalized = service.normalize_text(original)
    match = '✓' if normalized == expected else '✗'
    print(f'{match} "{original}"')
    print(f'  -> "{normalized}"')
    print()
