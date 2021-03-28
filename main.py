import requests
import tkinter as tk
from urllib.request import urlopen
from PIL import ImageTk, Image


class Pokedex:

  WIN_TITLE = "Pokedex"
  LOGO = "PokedexLogo.png"
  WIN_WIDTH = 1200
  WIN_HEIGHT = 700
  BACKGROUND = "PokeballBackground.png"
  DEFAULT_ICON = "PokeballDefault.png"

  def __init__(self):
    # main tkinter window
    self.window = tk.Tk()
    self.window.title(self.WIN_TITLE)
    self.window.iconphoto(False, tk.PhotoImage(file = "Assets/{l}".format(l = self.LOGO)))
    self.window.geometry("{W}x{H}".format(W = self.WIN_WIDTH, H = self.WIN_HEIGHT))
    self.window.resizable(False, False)

    self.pokemon = ""

    self.setup()

  def setup(self):
    '''
    Loads background image and entry box. Displays defualt logo.
    '''
    # background img
    bgPhoto = tk.PhotoImage(file = "Assets/{bg}".format(bg = self.BACKGROUND))
    self.bg = tk.Label(self.window, image = bgPhoto)
    self.bg.photo = bgPhoto
    self.bg.place(x = 0, y = 0, relwidth = 1, relheight = 1)

    # search feature
    entryFont = ("times", 18)
    entryBG = "white"
    self.entryFrame = tk.Frame(self.window, bg = entryBG)
    self.entryFrame.pack(anchor = "ne", padx = 10, pady = 10)
    tk.Label(self.entryFrame, text = "Enter a Pokemon's name (e.g. Togekiss)", font = entryFont, bg = entryBG).pack(side = "top", anchor = "center")
    self.entryBar = tk.Entry(self.entryFrame, font = entryFont)
    self.entryBar.pack(side = "left", expand = True)
    tk.Button(self.entryFrame, text = "Search", bg = entryBG, width = 8, height = 2, command = self.getEntry).pack(side = "right")

    self.displayInfo() # calls to display default icon and name box

  def updateRequest(self):
    '''
    Updates json data after new search.
    '''
    self.response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{self.pokemon}")
    self.data = self.response.json()    

  def getEntry(self):
    '''
    Updates pokemon and deletes current entry text.
    '''
    newEntry = self.entryBar.get()
    self.pokemon = newEntry.lower() # changes characters to lowercase
    self.entryBar.delete(0, "end") # clears entry box after user clicks search

    self.displayInfo()

  def displayInfo(self):
    '''
    Displays info for pokemon.
    '''
    self.updateRequest() # updates json with new pokemon entry

    bFont = ("times", 20)
    sFont = ("times", 18)
    bgColour = "white"

    # display pokemon's name, shows empty box by defualt
    pokemonName = tk.Label(self.window, text = self.pokemon.title(), font = bFont, bg = bgColour, relief = "solid", borderwidth = 5)
    pokemonName.place_forget()
    pokemonName.place(x = 450, y = 100, width = 300, height = 50)

    self.displaySprite()
    self.displayType(sFont, bgColour)
    self.displayAbilities(sFont, bgColour)
    self.displayStats(sFont, bgColour)
    self.displayWeight(sFont, bgColour)
    self.displayHeight(sFont, bgColour)
    self.displayId(bFont, bgColour)

  def displaySprite(self):
    if (self.pokemon == ""):
      # default sprite img
      defualtPhoto = tk.PhotoImage(file = "Assets/{dp}".format(dp = self.DEFAULT_ICON))
      self.dp = tk.Label(self.window, image = defualtPhoto, relief = "solid", borderwidth = 7)
      self.dp.photo = defualtPhoto
      self.dp.place(x = 100, y = 100, width = 300, height = 300)
    else:
      spriteURL = self.data["sprites"]["front_default"] # gets sprite URL
      spriteData = urlopen(spriteURL) # opens URL
      imageResize = Image.open(spriteData).resize((280, 280)) # resizes image
      spriteImage = ImageTk.PhotoImage(imageResize) # reads URL into Tk
      self.sprite = tk.Label(self.window, image = spriteImage, bg = "white", relief = "solid", borderwidth = 7)
      self.sprite.place_forget() # deletes previous sprite image
      self.sprite.photo = spriteImage
      self.sprite.place(x = 100, y = 100, width = 300, height = 300)

  def displayType(self, font, bg):
    pokemonType = []

    if (self.pokemon == ""):
      pass
    else:
      for t in range(len(self.data["types"])):
        pokemonType.append(self.data["types"][t]["type"]["name"])

      if (len(self.data["types"]) > 1):
        pokemonType = ", ".join(pokemonType)

      typeFrame = tk.Frame(self.window, bg = bg, relief = "solid", borderwidth = 5)
      tk.Label(typeFrame, text = "Type:", font = font, bg = bg).pack(side = "left")
      tk.Label(typeFrame, text = pokemonType, font = font, bg = bg).pack(pady = 7) # typing label
      typeFrame.place(x = 460, y = 180, width = 220, height = 50)
  
  def displayAbilities(self, font, bg):
    pokemonAbility = []
    pokemonAbilityHidden = []

    if (self.pokemon == ""):
      pass
    else:
      for a in range(len(self.data["abilities"])):
        # separates abilities from hidden one
        if (self.data["abilities"][a]["is_hidden"] == False):
          pokemonAbility.append(self.data["abilities"][a]["ability"]["name"])
        else: 
          pokemonAbilityHidden.append(self.data["abilities"][a]["ability"]["name"])

      if (len(pokemonAbility) > 1):
        pokemonAbility = ", ".join(pokemonAbility) # concatenate abilities and adds comma

      if (len(pokemonAbilityHidden) == 0):
        pokemonAbilityHidden = "(no hidden ability)" # if pokemon has no hidden ability
      elif (len(pokemonAbilityHidden) > 0):
        pokemonAbilityHidden = "{h} (hidden)".format(h = pokemonAbilityHidden.pop()) # adds hidden if has hidden ability
      
      abilityFrame = tk.Frame(self.window, bg = bg, relief = "solid", borderwidth = 5)
      tk.Label(abilityFrame, text = "Abilities:", font = font, bg = bg).pack(side = "left")
      tk.Label(abilityFrame, text = pokemonAbility, font = font, bg = bg).pack(side = "top", pady = 7) # normal abilities
      tk.Label(abilityFrame, text = pokemonAbilityHidden, font = font, bg = bg).pack(side = "bottom", pady = 7) # hidden abilities
      abilityFrame.place(x = 460, y = 250, width = 350, height = 100)

  def displayStats(self, font, bg):
    if (self.pokemon == ""):
      pass
    else: 
      hp = self.data["stats"][0]["base_stat"]
      attack = self.data["stats"][1]["base_stat"] 
      defense = self.data["stats"][2]["base_stat"] 
      spAttack = self.data["stats"][3]["base_stat"] 
      spDefense = self.data["stats"][4]["base_stat"] 
      speed = self.data["stats"][5]["base_stat"] 

      statWidth = 70
      statHeight = 180

      statFrame = tk.Frame(self.window, bg = bg, relief = "solid", borderwidth = 5)
      tk.Label(statFrame, text = "Base stats:", bg = bg, font = font).pack(side = "top", pady = 10)
      tk.Label(statFrame, text = "HP:\n\nAtk:\n\nDef:\n", bg = bg, font = font).place(x = 5, y = 60, width = statWidth, height = statHeight) # hp, atk, def
      tk.Label(statFrame, text = "{x}\n\n{y}\n\n{z}\n".format(x = hp, y = attack, z = defense), bg = bg, font = font).place(x = 65, y = 60, width = statWidth, height = statHeight)
      tk.Label(statFrame, text = "spAtk:\n\nspDef:\n\nSpd:\n", bg = bg, font = font).place(x = 150, y = 60, width = statWidth, height = statHeight) # spAtk, spDef, Spd
      tk.Label(statFrame, text = "{i}\n\n{j}\n\n{k}\n".format(i = spAttack, j = spDefense, k = speed), bg = bg, font = font).place(x = 220, y = 60, width = statWidth, height = statHeight)
      statFrame.place(x = 510, y = 420, width = 300, height = 250)

  def displayWeight(self, font, bg):
    if (self.pokemon == ""):
      pass
    else:
      pokemonWeight = (self.data["weight"]) / 10 # convert to kg

      weightFrame = tk.Frame(self.window, bg = bg, relief = "solid", borderwidth = 5)
      tk.Label(weightFrame, text = "Weight: {w} kg".format(w = pokemonWeight), font = font, bg = bg).pack(anchor = "center")
      weightFrame.place(x = 880, y = 580, width = 200, height = 50)

  def displayHeight(self, font, bg):
    if (self.pokemon == ""):
      pass
    else:
      pokemonHeight = (self.data["height"]) / 10 # convert to m

      heightFrame = tk.Frame(self.window, bg = bg, relief = "solid", borderwidth = 5)
      tk.Label(heightFrame, text = "Height: {h} m".format(h = pokemonHeight), font = font, bg = bg).pack(anchor = "center")
      heightFrame.place(x = 930, y = 490, width = 200, height = 50)

  def displayId(self, font, bg):
    if (self.pokemon == ""):
      pass
    else:
      idFrame = tk.Frame(self.window, bg = bg, relief = "solid", borderwidth = 5)
      tk.Label(idFrame, text = "#{id}".format(id = self.data["id"]), font = font, bg = bg).pack(anchor = "center", pady = 10)
      idFrame.place(x = 760, y = 100, width = 100, height = 50)


if __name__ == "__main__":
  Pokedex().window.mainloop()