using System;
using System.IO;
using System.Globalization;
using Microsoft.Xna.Framework;
using ProjectZ.InGame.Map;
using ProjectZ.InGame.SaveLoad;
using ProjectZ.InGame.Screens;
using ProjectZ.InGame.Things;

namespace ProjectZ
{
    public static class DiscordRpcBridge
    {
        private static double _rpcTimer = 0;
        private static string _statePath = null;

        public static string GetStatePath()
        {
            if (_statePath != null)
                return _statePath;

            try
            {
                if (Directory.Exists("/dev/shm"))
                {
                    _statePath = "/dev/shm/ladxhd_state.json";
                }
                else
                {
                    _statePath = Path.Combine(Path.GetTempPath(), "ladxhd_state.json");
                }
            }
            catch
            {
                _statePath = Path.Combine(Path.GetTempPath(), "ladxhd_state.json");
            }
            return _statePath;
        }

        public static void Update(Game1 game, GameTime gameTime)
        {
            _rpcTimer += gameTime.ElapsedGameTime.TotalSeconds;
            if (_rpcTimer < 0.25)
                return;

            _rpcTimer = 0;

            var gm = Game1.GameManager;
            bool inGame = Game1.ScreenManager?.CurrentScreenId == "GAME" 
                          && gm != null 
                          && MapManager.ObjLink != null 
                          && gm.MapManager?.CurrentMap != null;

            string mapName = inGame ? gm.MapManager.CurrentMap.MapName : "menu.map";
            float posX = inGame ? MapManager.ObjLink.EntityPosition.X : 0f;
            float posY = inGame ? MapManager.ObjLink.EntityPosition.Y : 0f;

            int maxHearts = 0;
            int currentHealth = 0;
            int rupees = 0;
            int instruments = 0;
            int seashells = 0;
            string tradeItem = "None";
            bool cleared = false;
            long totalSeconds = 0;
            int gridX = -1;
            int gridY = -1;

            if (inGame)
            {
                maxHearts = gm.MaxHearts;
                currentHealth = gm.CurrentHealth;
                cleared = gm.GameCleared;

                totalSeconds = (long)((gm.TotalPlaytime + gm.CurrentSessionPlaytime) * 60.0f);

                // Read live rupees: check item "ruby" first, then SaveManager, fallback to SaveStateManager
                var rubyItem = gm.GetItem("ruby");
                if (rubyItem != null)
                {
                    rupees = rubyItem.Count;
                }
                else if (gm.SaveManager != null)
                {
                    rupees = gm.SaveManager.GetInt("rubyCount", 0);
                }

                if (rupees == 0 && gm.SaveSlot >= 0 && gm.SaveSlot < SaveStateManager.SaveStates.Length && SaveStateManager.SaveStates[gm.SaveSlot] != null)
                {
                    rupees = SaveStateManager.SaveStates[gm.SaveSlot].CurrentRupees;
                }

                if (gm.SaveManager != null)
                {
                    seashells = gm.SaveManager.ShellCount;
                }

                var shellItem = gm.GetItem("shell") ?? gm.GetItem("seashell");
                if (shellItem != null)
                {
                    seashells = shellItem.Count;
                }

                if (gm.PlayerMapPosition.HasValue)
                {
                    gridX = gm.PlayerMapPosition.Value.X;
                    gridY = gm.PlayerMapPosition.Value.Y;
                }

                for (int i = 0; i < 8; i++)
                {
                    if (gm.GetItem("instrument" + i) != null)
                        instruments++;
                }

                string[] tradeNames = new string[]
                {
                    "Yoshi Doll", "Ribbon", "Dog Food", "Bananas", "Stick",
                    "Honeycomb", "Pineapple", "Hibiscus", "Letter", "Broom",
                    "Fishing Hook", "Necklace", "Mermaid's Scale", "Magnifying Glass"
                };
                for (int i = 13; i >= 0; i--)
                {
                    if (gm.GetItem("trade" + i) != null)
                    {
                        tradeItem = tradeNames[i];
                        break;
                    }
                }
            }

            string json = string.Format(
                CultureInfo.InvariantCulture,
                "{{\"InGame\":{0},\"Map\":\"{1}\",\"X\":{2:F2},\"Y\":{3:F2},\"GridX\":{4},\"GridY\":{5},\"CurrentHealth\":{6},\"MaxHearts\":{7},\"Rupees\":{8},\"Instruments\":{9},\"Seashells\":{10},\"TradeItem\":\"{11}\",\"Cleared\":{12},\"GameTime\":{13}}}",
                inGame ? "true" : "false",
                mapName,
                posX,
                posY,
                gridX,
                gridY,
                currentHealth,
                maxHearts,
                rupees,
                instruments,
                seashells,
                tradeItem,
                cleared ? "true" : "false",
                totalSeconds
            );

            try
            {
                string statePath = GetStatePath();
                string tmpPath = statePath + ".tmp";
                File.WriteAllText(tmpPath, json);
                File.Move(tmpPath, statePath, true);
            }
            catch { /* Ignore filesystem race conditions */ }
        }
    }
}
