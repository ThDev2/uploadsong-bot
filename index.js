import { Client, GatewayIntentBits, REST, Routes, SlashCommandBuilder } from 'discord.js';
import dotenv from 'dotenv';
dotenv.config();

const client = new Client({ intents: [GatewayIntentBits.Guilds] });

const commands = [
  new SlashCommandBuilder()
    .setName('uploadsong')
    .setDescription('Upload lagu ke GDPS')
    .addAttachmentOption(option =>
      option.setName('file')
        .setDescription('Lagu MP3')
        .setRequired(true))
].map(cmd => cmd.toJSON());

const rest = new REST({ version: '10' }).setToken(process.env.TOKEN);

(async () => {
  try {
    console.log('Mengupdate slash command...');
    await rest.put(
      Routes.applicationGuildCommands(process.env.CLIENT_ID, process.env.GUILD_ID),
      { body: commands }
    );
    console.log('Command berhasil diupdate!');
  } catch (err) {
    console.error(err);
  }
})();

client.on('interactionCreate', async interaction => {
  if (!interaction.isChatInputCommand()) return;
  if (interaction.commandName === 'uploadsong') {
    const file = interaction.options.getAttachment('file');
    if (file.contentType !== 'audio/mpeg') {
      return interaction.reply({ content: 'Hanya file MP3 yang diperbolehkan.', ephemeral: true });
    }

    // Simulasi upload ke GDPS
    await interaction.reply(`Lagu "${file.name}" berhasil diunggah! (simulasi)`);
  }
});

client.once('ready', () => {
  console.log(`Bot aktif sebagai ${client.user.tag}`);
});

client.login(process.env.TOKEN);
